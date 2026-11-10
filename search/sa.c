// Simulated annealing for short sequences containing all permutations of [n] as subsequences.
// Objective: exact number of permutations NOT embedded, maintained by an incremental subset DP.
//   P[q][A] = number of orderings of set A whose greedy (leftmost) embedding ends at index <= q.
//   Row q (symbol x): P[q][A] = P[q-1][A] + (x in A ? P[q-1][A-x] - P[prev_x(q)][A-x] : 0)
// A change at index p only invalidates rows >= p.
// usage: sa n Ltarget seed seconds [initfile]
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <math.h>
#include <time.h>
typedef uint64_t u64;
static int n, L, FULL; static size_t SZ; static u64 fact;
static int s[1024], t[1024];
static u64 **P, **Q, *B0, *Z;
static u64 rs;
static inline u64 rnd(void){ rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs; }
static inline double urnd(void){ return (rnd() >> 11) * (1.0/9007199254740992.0); }

static u64 eval_from(const int *tt, int Lt, int p0){
    int last[64]; for(int x=0;x<n;x++) last[x]=-1;
    for(int q=0;q<p0;q++) last[tt[q]]=q;
    for(int q=p0;q<Lt;q++){
        int x=tt[q]; size_t xb=(size_t)1<<x;
        const u64 *old = (q==0)?B0:((q-1>=p0)?Q[q-1]:P[q-1]);
        const u64 *pr = (last[x]<0)?Z:((last[x]>=p0)?Q[last[x]]:P[last[x]]);
        u64 *nw=Q[q];
        memcpy(nw,old,SZ*sizeof(u64));
        for(size_t hi=0;hi<SZ;hi+=2*xb){
            u64 *d=nw+hi+xb; const u64 *o=old+hi, *r=pr+hi;
            for(size_t lo=0;lo<xb;lo++) d[lo]+=o[lo]-r[lo];
        }
        last[x]=q;
    }
    const u64 *fin=(Lt-1>=p0)?Q[Lt-1]:P[Lt-1];
    return fact-fin[FULL];
}
static void accept_from(int Lt,int p0){
    for(int q=p0;q<Lt;q++){ u64 *tmp=P[q]; P[q]=Q[q]; Q[q]=tmp; }
    memcpy(s,t,sizeof(int)*Lt); L=Lt;
}
static void prseq(FILE *f,const int *a,int len){
    for(int i=0;i<len;i++) fprintf(f,"%d%s",a[i],i+1<len?" ":"\n");
}
static int adj_ok(const int *a,int len){ for(int i=0;i+1<len;i++) if(a[i]==a[i+1]) return 0; return 1; }

int main(int argc,char**argv){
    if(argc<5){ fprintf(stderr,"usage: sa n Ltarget seed seconds [initfile]\n"); return 1; }
    n=atoi(argv[1]); int Ltarget=atoi(argv[2]); rs=88172645463325252ULL ^ ((u64)atoll(argv[3])*0x9E3779B97F4A7C15ULL); double tlimit=atof(argv[4]);
    for(int i=0;i<20;i++) rnd();
    FULL=(1<<n)-1; SZ=(size_t)1<<n; fact=1; for(int i=2;i<=n;i++) fact*=i;
    int L0;
    if(argc>5){
        FILE *f=fopen(argv[5],"r"); L0=0; int v; while(fscanf(f,"%d",&v)==1) s[L0++]=v; fclose(f);
    } else {
        // Schoenfield construction, length (n-1)^2+3
        L0=(n-1)*(n-1)+3;
        for(int i=1;i<=L0;i++){
            int d;
            if(i<=n) d=i; else if((i-2)%(n-1)==0) d=1; else d=(((long)(i-1)*(n-2)/(n-1))%(n-1))+2;
            s[i-1]=d-1;
        }
    }
    int maxL=L0+2;
    P=malloc(sizeof(u64*)*maxL); Q=malloc(sizeof(u64*)*maxL);
    for(int q=0;q<maxL;q++){ P[q]=malloc(SZ*sizeof(u64)); Q[q]=malloc(SZ*sizeof(u64)); }
    B0=calloc(SZ,sizeof(u64)); Z=calloc(SZ,sizeof(u64)); B0[0]=1;
    L=L0; memcpy(t,s,sizeof(int)*L);
    u64 miss=eval_from(t,L,0); accept_from(L,0);
    fprintf(stderr,"n=%d start L=%d missing=%llu target=%d\n",n,L,(unsigned long long)miss,Ltarget);
    clock_t c0=clock();
    double T0=0.30,T1=0.004; long cycle=(n<=9)?400000:(n<=10?1500000:(n<=11?1200000:800000));
    long it=0, itL=0; u64 best=miss; int beststuck=0;
    static int bs[1024]; int bL=L; memcpy(bs,s,sizeof(int)*L);
    while(1){
        if(miss==0){
            printf("FOUND n=%d L=%d : ",n,L); prseq(stdout,s,L); fflush(stdout);
            if(L<=Ltarget) break;
            // delete the position that leaves the fewest missing permutations
            u64 bm=~0ULL; int bi=-1; int cntb=0;
            for(int i=0;i<L;i++){
                memcpy(t,s,sizeof(int)*i); memcpy(t+i,s+i+1,sizeof(int)*(L-1-i));
                if(!adj_ok(t,L-1)) continue;
                u64 m=eval_from(t,L-1,i);
                if(m<bm){ bm=m; bi=i; cntb=1; } else if(m==bm){ cntb++; if(rnd()%cntb==0) bi=i; }
            }
            memcpy(t,s,sizeof(int)*bi); memcpy(t+bi,s+bi+1,sizeof(int)*(L-1-bi));
            miss=eval_from(t,L-1,bi); accept_from(L-1,bi);
            fprintf(stderr,"[%.0fs] now L=%d missing=%llu\n",(double)(clock()-c0)/CLOCKS_PER_SEC,L,(unsigned long long)miss);
            itL=0; best=miss; continue;
        }
        if((it&1023)==0){
            double el=(double)(clock()-c0)/CLOCKS_PER_SEC;
            if(el>tlimit) break;
        }
        it++; itL++;
        double frac=(double)(itL%cycle)/cycle;
        double T=T0*pow(T1/T0,frac);
        if(itL%cycle==0){
            fprintf(stderr,"[%.0fs] L=%d cycle done: cur missing=%llu best=%llu\n",(double)(clock()-c0)/CLOCKS_PER_SEC,L,(unsigned long long)miss,(unsigned long long)best);
            beststuck++;
        }
        memcpy(t,s,sizeof(int)*L);
        int p0; double r=urnd();
        if(r<0.5){
            int p=rnd()%L; int c=rnd()%n;
            if(c==s[p]||(p>0&&c==s[p-1])||(p+1<L&&c==s[p+1])) continue;
            t[p]=c; p0=p;
        } else if(r<0.75){
            int p=rnd()%(L-1);
            t[p]=s[p+1]; t[p+1]=s[p];
            if((p>0&&t[p]==t[p-1])||(p+2<L&&t[p+1]==t[p+2])) continue;
            p0=p;
        } else {
            int i=rnd()%L, j=rnd()%L, c=rnd()%n;
            // remove index i, then insert c at index j of the shortened sequence
            int k=0; for(int q=0;q<L;q++) if(q!=i) t[k++]=s[q];
            memmove(t+j+1,t+j,sizeof(int)*(L-1-j)); t[j]=c;
            if(!adj_ok(t,L)) continue;
            p0=i<j?i:j;
        }
        u64 m=eval_from(t,L,p0);
        double d=log1p((double)m)-log1p((double)miss);
        if(d<=0 || urnd()<exp(-d/T)){
            accept_from(L,p0); miss=m;
            if(miss<best){ best=miss; }
        }
    }
    fprintf(stderr,"end: L=%d missing=%llu iters=%ld\n",L,(unsigned long long)miss,it);
    return 0;
}
