# Quick overview of our DNS/DoH architecture

A channel goes to `example.com` and needs to resolve it

[nsDNSService::AsyncResolveInternal](https://searchfox.org/mozilla-central/rev/b4e790d05f5a146d186c238bac5601a553581d23/netwerk/dns/nsDNSService2.cpp#847) -> [nsHostResolver](https://searchfox.org/mozilla-central/rev/b4e790d05f5a146d186c238bac5601a553581d23/netwerk/dns/nsHostResolver.cpp#899,904) ([thread pool](https://searchfox.org/mozilla-central/rev/b4e790d05f5a146d186c238bac5601a553581d23/netwerk/dns/nsHostResolver.h#554)) -> blocking calls [getaddrinfo](https://searchfox.org/mozilla-central/rev/b4e790d05f5a146d186c238bac5601a553581d23/netwerk/dns/nsHostResolver.cpp#2054,2071).

nsHostResolver has a [cache](https://searchfox.org/mozilla-central/rev/b4e790d05f5a146d186c238bac5601a553581d23/netwerk/dns/nsHostResolver.h#544) (hashtable) of nsHostRecord (cached DNS entries)

When TRR (Trusted Recursive Resolver - our name for the client part of DoH) is [enabled](https://searchfox.org/mozilla-central/rev/b4e790d05f5a146d186c238bac5601a553581d23/netwerk/dns/TRRService.cpp#99), instead of putting the request in the queue for the threadpool to resolve, we pass it to [TRR.cpp](https://searchfox.org/mozilla-central/rev/b4e790d05f5a146d186c238bac5601a553581d23/netwerk/dns/TRR.cpp#164) that resolves it, meaning it is encoded, sent over the DoH channel, we [decode](https://searchfox.org/mozilla-central/rev/b4e790d05f5a146d186c238bac5601a553581d23/netwerk/dns/TRR.cpp#927) the response, and [build an nsHostRecord](https://searchfox.org/mozilla-central/rev/b4e790d05f5a146d186c238bac5601a553581d23/netwerk/dns/TRR.cpp#877) that we [pass pack to the caller](https://searchfox.org/mozilla-central/rev/b4e790d05f5a146d186c238bac5601a553581d23/netwerk/dns/nsHostResolver.cpp#1693) (via callback), and it's also put in the nsHostResolver cache.

If a connection using an IP obtained via TRR fails to be established, we blacklist that host name and fallback to regular DNS.

https://daniel.haxx.se/blog/2018/06/03/inside-firefoxs-doh-engine/

A pref that is not included in the blog post (domains that we never resolve with TRR) - network.trr.excluded-domains

Main TRR bug: https://bugzilla.mozilla.org/show_bug.cgi?id=doh

open TRR bugs: https://bugzilla.mozilla.org/buglist.cgi?quicksearch=%5Btrr%5D

