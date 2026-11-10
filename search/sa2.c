// sa2: heat-bath annealing with an O(n 2^n) exact "split" evaluator.
//
// F[q][A] = number of orderings of the set A that are subsequences of the prefix s[0..q]
// T[q][B] = number of orderings of the set B that are subsequences of the suffix s[q..L-1]
//   F[q][A] = F[q-1][A] + [x in A] (F[q-1][A-x] - F[prev_x(q)][A-x]),  x = s[q]
//   T[q][B] = T[q+1][B] + [x in B] (T[q+1][B-x] - T[next_x(q)+1][B-x])
// Split identity at any cut point c (all permutations embedded in s, counted by the maximal
// prefix alpha (set A) whose leftmost embedding ends before c, and the next letter y):
//   emb = F[c-1][full] + sum_y sum_{A not containing y} (F[c-1][A] - F[last_y(c)][A]) * T[next_y(c)+1][full-A-y]
// Replacing the symbol at index p by y costs nothing extra: use T[p+1] instead of T[next_y+1].
//
// usage: sa2 n Ltarget seed seconds [initfile] [T0 T1 sweeps_per_cycle]
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <math.h>
#include <time.h>
typedef uint64_t u64;
#ifndef CT
#define CT uint64_t
#endif
typedef CT cnt_t;   // counts are kept modulo 2^bits; 'missing' is assumed < 2^bits
static int n, L, FULL, maxL; static size_t SZ; static u64 fact;
static int s[2048];
static cnt_t **Fr, **Tr, *Z; static cnt_t factm;        // Fr[q+1] = F[q] (q=-1..L-1) ; Tr[q] = T[q] (q=0..L)
static cnt_t *G[8];                 // scratch rows for window moves
static int fv, tv;                // F rows valid for q<fv ; T rows valid for q>=tv
static u64 rs;
static inline u64 rnd(void){ rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs; }
static inline double urnd(void){ return (rnd() >> 11) * (1.0/9007199254740992.0); }
#define F(q) (Fr[(q)+1])

static inline void row_update(cnt_t *nw, const cnt_t *old, const cnt_t *pr, int x){
    size_t xb=(size_t)1<<x;
    memcpy(nw,old,SZ*sizeof(cnt_t));
    for(size_t hi=0;hi<SZ;hi+=2*xb){
        cnt_t *d=nw+hi+xb; const cnt_t *o=old+hi, *r=pr+hi;
        for(size_t lo=0;lo<xb;lo++) d[lo]+=o[lo]-r[lo];
    }
}
// T rows are stored in complemented indexing: Tr[q][C] = #orderings of (full minus C) embedded in s[q..]
static inline void row_update_c(cnt_t *nw, const cnt_t *old, const cnt_t *pr, int x){
    size_t xb=(size_t)1<<x;
    memcpy(nw,old,SZ*sizeof(cnt_t));
    for(size_t hi=0;hi<SZ;hi+=2*xb){
        cnt_t *d=nw+hi; const cnt_t *o=old+hi+xb, *r=pr+hi+xb;
        for(size_t lo=0;lo<xb;lo++) d[lo]+=o[lo]-r[lo];
    }
}
static void fwd_row(int q){ int x=s[q]; int pv=-1; for(int i=q-1;i>=0;i--) if(s[i]==x){pv=i;break;}
    row_update(F(q),F(q-1),pv<0?Z:F(pv),x); }
static void bwd_row(int q){ int x=s[q]; int nx=-1; for(int i=q+1;i<L;i++) if(s[i]==x){nx=i;break;}
    row_update_c(Tr[q],Tr[q+1],nx<0?Z:Tr[nx+1],x); }
static inline void ensF(int p){ while(fv<p){ fwd_row(fv); fv++; } }
static inline void ensT(int q){ while(tv>q){ bwd_row(tv-1); tv--; } }

// sum_{A not containing y} (Fa[A]-Fb[A]) * Ta[A+yb]   (Ta complemented-indexed => entry for full-A-y)
static inline void dot2(const cnt_t *Fa,const cnt_t *Fb,const cnt_t *Ta,const cnt_t *Tb,int y,cnt_t *ra,cnt_t *rb){
    size_t yb=(size_t)1<<y; cnt_t sa=0,sb=0;
    for(size_t hi=0;hi<SZ;hi+=2*yb){
        const cnt_t *a=Fa+hi,*b=Fb+hi; const cnt_t *ta=Ta+hi+yb, *tb=Tb+hi+yb;
        for(size_t lo=0;lo<yb;lo++){ cnt_t u=a[lo]-b[lo]; sa+=u*ta[lo]; sb+=u*tb[lo]; }
    }
    *ra=sa; *rb=sb;
}
static inline cnt_t dot1(const cnt_t *Fa,const cnt_t *Fb,const cnt_t *Ta,int y){
    size_t yb=(size_t)1<<y; cnt_t sa=0;
    for(size_t hi=0;hi<SZ;hi+=2*yb){
        const cnt_t *a=Fa+hi,*b=Fb+hi; const cnt_t *ta=Ta+hi+yb;
        for(size_t lo=0;lo<yb;lo++){ cnt_t u=a[lo]-b[lo]; sa+=u*ta[lo]; }
    }
    return sa;
}
// evaluate all symbols at site p, and deletion of site p.  emb[c] for c in 0..n-1, *embdel
static void site_eval(int p,cnt_t *emb,cnt_t *embdel){
    ensF(p); ensT(p+1);
    int last[64],next[64];
    for(int y=0;y<n;y++){ last[y]=-1; next[y]=-1; }
    for(int i=0;i<p;i++) last[s[i]]=i;
    for(int i=L-1;i>p;i--) next[s[i]]=i;
    const cnt_t *Fa=F(p-1), *Tn=Tr[p+1];
    cnt_t base=Fa[FULL], tot=0; cnt_t sf[64],sn[64];
    for(int y=0;y<n;y++){
        if(last[y]==p-1 && p>0){ sf[y]=0; sn[y]=0; continue; }
        const cnt_t *Fb=last[y]<0?Z:F(last[y]);
        const cnt_t *Tf=next[y]<0?Z:Tr[next[y]+1];
        dot2(Fa,Fb,Tf,Tn,y,&sf[y],&sn[y]);
        tot+=sf[y];
    }
    for(int c=0;c<n;c++) emb[c]=base+tot-sf[c]+sn[c];
    *embdel=base+tot;
}
// evaluate replacing window s[p..p+w-1] by content nc[0..w-1]
static cnt_t window_eval(int p,int w,const int *nc){
    ensF(p); ensT(p+w);
    int last[64],next[64],lastw[64];
    for(int y=0;y<n;y++){ last[y]=-1; next[y]=-1; lastw[y]=-1; }
    for(int i=0;i<p;i++) last[s[i]]=i;
    for(int i=L-1;i>=p+w;i--) next[s[i]]=i;
    for(int j=0;j<w;j++){
        int x=nc[j];
        const cnt_t *old = j==0?F(p-1):G[j-1];
        const cnt_t *pr = lastw[x]>=0?G[lastw[x]]:(last[x]<0?Z:F(last[x]));
        row_update(G[j],old,pr,x);
        lastw[x]=j;
    }
    const cnt_t *Fa=G[w-1]; cnt_t emb=Fa[FULL];
    for(int y=0;y<n;y++){
        if(lastw[y]==w-1) continue;
        if(next[y]<0) continue;
        const cnt_t *Fb = lastw[y]>=0?G[lastw[y]]:(last[y]<0?Z:F(last[y]));
        emb+=dot1(Fa,Fb,Tr[next[y]+1],y);
    }
    return emb;
}
static u64 full_missing(void){ fv=0; tv=L; ensF(L); ensT(0); return (u64)(cnt_t)(factm-F(L-1)[FULL]); }
static void prseq(FILE *f){ for(int i=0;i<L;i++) fprintf(f,"%d%s",s[i],i+1<L?" ":"\n"); }

int main(int argc,char**argv){
    if(argc<5){ fprintf(stderr,"usage: sa2 n Ltarget seed seconds [initfile|-] [T0 T1 sweeps]\n"); return 1; }
    n=atoi(argv[1]); int Ltarget=atoi(argv[2]); rs=88172645463325252ULL ^ ((u64)atoll(argv[3])*0x9E3779B97F4A7C15ULL); double tlimit=atof(argv[4]);
    for(int i=0;i<20;i++) rnd();
    FULL=(1<<n)-1; SZ=(size_t)1<<n; fact=1; for(int i=2;i<=n;i++) fact*=i;
    if(argc>5 && strcmp(argv[5],"-")!=0){
        FILE *f=fopen(argv[5],"r"); L=0; int v; while(fscanf(f,"%d",&v)==1) s[L++]=v; fclose(f);
    } else {
        L=(n-1)*(n-1)+3;
        for(int i=1;i<=L;i++){
            int d;
            if(i<=n) d=i; else if((i-2)%(n-1)==0) d=1; else d=(((long)(i-1)*(n-2)/(n-1))%(n-1))+2;
            s[i-1]=d-1;
        }
    }
    double T0=0.25,T1=0.01; int cyc=300;
    if(argc>8){ T0=atof(argv[6]); T1=atof(argv[7]); cyc=atoi(argv[8]); }
    maxL=L+1;
    factm=(cnt_t)fact;
    Fr=malloc(sizeof(cnt_t*)*(maxL+2)); Tr=malloc(sizeof(cnt_t*)*(maxL+2));
    for(int q=0;q<maxL+2;q++){ Fr[q]=calloc(SZ,sizeof(cnt_t)); Tr[q]=calloc(SZ,sizeof(cnt_t)); }
    for(int j=0;j<8;j++) G[j]=calloc(SZ,sizeof(cnt_t));
    Z=calloc(SZ,sizeof(cnt_t));
    F(-1)[0]=1; Tr[L][FULL]=1;
    u64 miss=full_missing();
    fprintf(stderr,"n=%d start L=%d missing=%llu target=%d T0=%g T1=%g cyc=%d\n",n,L,(unsigned long long)miss,Ltarget,T0,T1,cyc);
    // self-test of the split evaluator against the full DP
    { cnt_t emb[64],ed; for(int k=0;k<3;k++){ int p=rnd()%L; site_eval(p,emb,&ed);
        if((u64)(cnt_t)(factm-emb[s[p]])!=miss){ fprintf(stderr,"SELFTEST FAIL site %d\n",p); return 2; } } }
    struct timespec ts0; clock_gettime(CLOCK_MONOTONIC,&ts0);
    #define ELAPSED() ({ struct timespec t1_; clock_gettime(CLOCK_MONOTONIC,&t1_); (t1_.tv_sec-ts0.tv_sec)+1e-9*(t1_.tv_nsec-ts0.tv_nsec); })
    long sweep=0, sweepL=0; u64 best=miss; int dir=1;
    cnt_t emb[64],ed; double wgt[64];
    while(1){
        if(miss==0){
            u64 chk=full_missing();
            if(chk!=0){ fprintf(stderr,"internal mismatch\n"); return 3; }
            printf("FOUND n=%d L=%d : ",n,L); prseq(stdout); fflush(stdout);
            if(L<=Ltarget) break;
            // choose deletion with fewest missing permutations
            u64 bm=~0ULL; int bi=-1,cntb=0;
            for(int p=0;p<L;p++){
                site_eval(p,emb,&ed); u64 m=(u64)(cnt_t)(factm-ed);
                if(p>0&&p+1<L&&s[p-1]==s[p+1]) continue;
                if(m<bm){ bm=m; bi=p; cntb=1; } else if(m==bm){ cntb++; if(rnd()%cntb==0) bi=p; }
            }
            memmove(s+bi,s+bi+1,sizeof(int)*(L-1-bi));
            // shift T rows: old row q (q>=bi+1) becomes row q-1
            cnt_t *sv=Tr[bi]; for(int q=bi;q<L;q++) Tr[q]=Tr[q+1]; Tr[L]=sv;
            if(fv>bi) fv=bi;
            { int tvn=(tv>bi+1?tv:bi+1)-1; tv=tvn; }
            L--; miss=bm; best=miss; sweepL=0;
            fprintf(stderr,"[%.0fs] now L=%d missing=%llu\n",ELAPSED(),L,(unsigned long long)miss);
            continue;
        }
        if(ELAPSED()>tlimit) break;
        double frac=(double)(sweepL%cyc)/cyc; double T=T0*pow(T1/T0,frac);
        for(int k=0;k<L && miss!=0;k++){
            int p = dir>0 ? k : L-1-k;
            // heat-bath point update
            site_eval(p,emb,&ed);
            double emin=1e300; double e[64];
            for(int c=0;c<n;c++){
                if((p>0&&c==s[p-1])||(p+1<L&&c==s[p+1])){ e[c]=1e300; continue; }
                e[c]=log1p((double)(cnt_t)(factm-emb[c])); if(e[c]<emin) emin=e[c];
            }
            double tw=0; for(int c=0;c<n;c++){ wgt[c]=(e[c]>=1e299)?0:exp(-(e[c]-emin)/T); tw+=wgt[c]; }
            double r=urnd()*tw; int c=0; for(;c<n-1;c++){ r-=wgt[c]; if(r<0) break; }
            while(wgt[c]==0) c=(c+1)%n;
            if(c!=s[p]){ s[p]=c; if(fv>p) fv=p; if(tv<p+1) tv=p+1; }
            miss=(u64)(cnt_t)(factm-emb[c]);
            if(miss<best) best=miss;
            if(miss==0) break;
            // window rotation move
            if((rnd()&1)){
                int w=2+rnd()%3; if(p+w>L) continue;
                int nc[8];
                if(rnd()&1){ for(int j=0;j<w-1;j++) nc[j]=s[p+j+1]; nc[w-1]=s[p]; }
                else { nc[0]=s[p+w-1]; for(int j=1;j<w;j++) nc[j]=s[p+j-1]; }
                int ok=1; for(int j=0;j+1<w;j++) if(nc[j]==nc[j+1]) ok=0;
                if(p>0&&nc[0]==s[p-1]) ok=0; if(p+w<L&&nc[w-1]==s[p+w]) ok=0;
                if(!ok) continue;
                u64 m=(u64)(cnt_t)(factm-window_eval(p,w,nc));
                double d=log1p((double)m)-log1p((double)miss);
                if(d<=0||urnd()<exp(-d/T)){
                    for(int j=0;j<w;j++) s[p+j]=nc[j];
                    if(fv>p) fv=p; if(tv<p+w) tv=p+w; miss=m; if(miss<best) best=miss;
                }
            }
        }
        dir=-dir; sweep++; sweepL++;
        if(sweepL%cyc==0)
            fprintf(stderr,"[%.0fs] L=%d cycle %ld: cur missing=%llu best=%llu\n",ELAPSED(),L,sweepL/cyc,(unsigned long long)miss,(unsigned long long)best);
    }
    fprintf(stderr,"end: L=%d missing=%llu sweeps=%ld time=%.0f\n",L,(unsigned long long)miss,sweep,ELAPSED());
    return 0;
}
