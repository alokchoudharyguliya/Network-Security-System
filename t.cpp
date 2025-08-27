
#include <bits/stdc++.h>
#define fio                   \
ios_base::sync_with_stdio(0); \
cin.tie(0);                   \
cout.tie(0);
#define debug(_) cout << #_ << " is " << _ << '\n';
using namespace std;
using ll=long long;
using ld=long double;
const ll mod = 1e9 + 7;
const ll N = 2e5 + 10;
const ll inf = 1e9;
const ll linf = 1e18;
int main()
{
    fio;
    int t;
    cin >> t;
    while (t--)
    {
        int n;
        cin>>n;
        string s;
        cin>>s;
        bool ans=true;
        int cntZero=0;
        int cntOne=0;
        int l=0,r=0;
        for(int i=0;i<s.size();i++)
        {
            if(s[i]=='0')
            cntZero++;
        }
        if(cntZero==s.size()){
            cout<<"Yes"<<"\n";
            continue;   
        }
        while(r<s.size()){
            if(s[r]=='1')
            {
                r++;
            }
            else{
                // cout<<r-l;
                if((r-l)<3&&r!=l){
                        // cout<<r<<","<<l;
                        ans=false;
                        break;
                }
                r++;
                l=r;
            }
        }
        if(s[r-1]==1)
        if(r-l<3)ans=false;
        ans?cout<<"Yes"<<"\n":cout<<"No"<<"\n";
    }
    return 0;
}