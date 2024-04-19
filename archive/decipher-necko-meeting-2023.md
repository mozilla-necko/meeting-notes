### Dec 15, 2023

- **Documentation updates**
  - [Phabricator: D195754](https://phabricator.services.mozilla.com/D195754)
  - [Bugzilla: 1773234](https://bugzilla.mozilla.org/show_bug.cgi?id=1773234)
- **Manuel to discuss**
  - [Bugzilla: 1868987](https://bugzilla.mozilla.org/show_bug.cgi?id=1868987)
  - **Problem**
    - We are uploading data and don’t get any response for the ping frame and the connection is closed.
    - While sending http2 ping and there is some data in the buffer. Data before the ping is sent but not the ping. 
  - **Observation**
  - **Possible root causes**
    - [Randell] Variant of buffer bloat in the router. 
  - **Approach**
    - Send ping packet only when we don't receive any data back and are not sending any data.

- **Do Team meetings into etherpads again and share results publicly?**
  - [Meeting Notes Repository](https://github.com/mozilla-necko/meeting-notes)
  - Concerns:
    - Can leak security issues to public
    - MoCo specific confidential information can be leaked.
    - Bug lists can be problematic.
  - Suggestions:
    - Subset of information (project status updates/round table updates) can be made public. 
    - Separate meeting notes into team-specific and separate documents to capture project status/round table.
    - Put priority queue into the matrix channel
    - Put a good first bug in the matrix channel
    - [Team Resources](https://wiki.mozilla.org/Networking#Team_resources)


### Nov 17, 2023

- **Review Ed’s [AsyncOpen to OnDataAvailable](https://docs.google.com/document/d/1EDkFfKM-chvJfOAuVWnqiT9rTzwD0M2k4ZUbOh_KOx0/edit) code path**
- **Request prioritization, HTTP/2, HTTP/3 by resource type**
- [**Network Priorities**](https://docs.google.com/document/d/1eGR-k8ZDBH-nTqnJm0bBlSJsQrw67hfkAopVjGXTW7M/edit)
- **Discuss channel event queue**
  
#### ChannelEventQueue
- **What is a [ChannelEventQueue](https://searchfox.org/mozilla-central/rev/b58777ee2097f4e144865260e6f110bdfa1bb3f9/netwerk/ipc/ChannelEventQueue.h#106)?**
  - Class for serializing execution of events among various thread targets

- **What events are dispatched to event queues?**
  - It is used to queue events in an ordered manner to be run on target threads.
  - Mainly OnStartRequest/OnDataAvaialble/OnDataFinishedF/OnStopRequest events
  - Current [usage](https://searchfox.org/mozilla-central/search?q=symbol:T_mozilla%3A%3Anet%3A%3AChannelEventQueue&redirect=false) - HttpChannelChild, HttpChannelParent 
  - Our focus of today’s discussion is HttpChannelChild class

- **Functioning of the queue**
  -[ Dispatch a runnable with a target to run](https://searchfox.org/mozilla-central/rev/b58777ee2097f4e144865260e6f110bdfa1bb3f9/netwerk/ipc/ChannelEventQueue.h#220-222)
  - Queue the events for the following [cases](https://searchfox.org/mozilla-central/rev/b58777ee2097f4e144865260e6f110bdfa1bb3f9/netwerk/ipc/ChannelEventQueue.h#220-222) -
    - Queue is suspended
    - Force queueing enabled ([AutoEventQueuer](https://searchfox.org/mozilla-central/rev/b58777ee2097f4e144865260e6f110bdfa1bb3f9/netwerk/ipc/ChannelEventQueue.h#344))
    - Events are executed in another thread
    - Queue is non-empty
  - Events on the same target thread are run
  - Events on other target threads are dispatched to the target thread.
  - Events for a thread are executed in their queued orders.
  - Events for a thread are dispatched in their queued order.

- **How do we ensure that the events in different threads are executed orderly?**
  - OnStartRequest target -> Main Thread
  - OnDataAvailable target -> ODA target (socket thread/listener thread)
  - OnDataFinished target -> ODA target
  - OnStopRequest target -> Main Thread 

- **How do we guarantee OnStartRequest is executed before OnDataAvailable?**
  - While flushing (executing the queued events), if the event does not belong to the same thread, suspend the queue execution.
  - Resume the event execution when the remote target thread executes the event. This is done by passing a callback to the target thread to execute a [callback](https://searchfox.org/mozilla-central/rev/b58777ee2097f4e144865260e6f110bdfa1bb3f9/netwerk/ipc/ChannelEventQueue.cpp#143) on the event queue. The callback resumes execution of events from the queue. The top event belongs to the current executing thread and hence can run synchronously.

### Oct 6, 2023
- **HTTP Cache Lightning talk**

### Sep 29, 2023
- **Cache Overview**
  - nsHttpChannel and caches
  - Overview of various caches in Necko
    - Auth Cache
    - DNS Cache 
    - HTTP Cache
- **HTTP Cache**
  - What do we cache?
    - Responses/Headers 
  - Cache internals, Interfaces - good source
- **Cache Interfaces**
  - nsICacheStorage - opening caches
  - nsICacheEntryOpenCallback - 2 callbacks on opening a cache entry
  - nsICacheEntry.idl - interfacing with the cache entry
- **Important call sites for caches for nsHttpChannel**
  - Reading Cache Entry
  - Updating Cache Entry
  - Cache member variables
  - Reading a Cache Entry when opening a channel
  - Opening a cache Entry
  - Callbacks On Opening a Cache Entry
  - nsHttpChannel::OnCacheEntryCheck
    - Decide if the data is okay and can be used or send network request
  - nsHttpChannel::OnCacheEntryAvailable
    - Read the cached data
- **How are listeners notified of OnStart/OnStopRequest**
- **Writing to cache**
  - ContinueProcessNormal
  - ContinueProcessResponse4

- **Auth Cache**
  - 401/407 response means requests needs authentication
  - Response is checked for the kind of authentication we need
  - Authenticator is initiated based on the response message
  - What do we cache?
    - Credentials
    - Session state
    - Challenge
  - Storage for auth cache
    - Main memory cache

- **DNS Cache**
  - What do we cache?
    - DNS records, entries
  - Consumers call AsyncResolve for DNS resolution
  - Check mRecordDB if we have the key
  - Keys are host, trrserver, address type, family, origin suffix, private browsing flags
  - Threads are dispatched
  - DoH requests to TRR
  - We have a mechanism to avoid congestion on the main thread of the parent process, right? How does that work?

### Sep 8, 2023
- **XPCOM tutorial**
  - [Bugzilla: 1223177](https://bugzilla.mozilla.org/show_bug.cgi?id=1223177)
- **XPCOM vs XPIPDL**
  - Should the caller and callee reside in the same process for XPCOM?
- **Steps for writing a new interface**
- **Using the interfaces do_QueryInterface**
- **What do each of these macros do?**
  - NS_DECL_NSISTREAMLISTENER: Declares OnDataAvailable 
  - NS_IMPL_ISUPPORTS: Defines default nsISupports methods, like AddRef, Release, QueryInterface
- **nsComPtr and RefPtr are NOT threadsafe**, though internally the ref counter IS
- **Various uses of interface maps?**
- **Overriding the default nsISupport methods on a case by case basis is possible to do manually or using existing macros. Here is an example of passing a destructor helper function to similarly default implementation of Release(). Note that this is used to dispatch deletion to a target thread.**
- **When to define custom accessors?**
  - We need this for querying the concrete object
- **Why static IID accessor NS_DECLARE_STATIC_IID_ACCESSOR?**
  - We need this for querying the concrete object
- **NS_DECL_ISUPPORTS_INHERITED**
- **NS_IMPL_ISUPPORTS_INHERITED**
  - [Useful link](http://udn.realityripple.com/docs/Mozilla/Tech/XPCOM/Guide)


## Aug 18, 2023

- **Functional Overview of Proxy**
  - What are the kinds of proxies we support?
    - HTTP/HTTPS/SOCKS
  - Proxy UI Settings
    - Where do we retrieve the configuration for proxy?
      - UI/Pref
      - OS system API for retrieving the proxy configuration
      - PAC - URL to file (JS based) where we fetch proxy related information
        - Example:
          - PAC Manager loads the PAC URL and stores the proxy information in memory
          - `nsHttpChannel` requests proxy service for proxy information
          - `nsIProxyService` returns proxyInfo (which also contains secondary proxyInfo for backup)
          - UI pref for selecting the priority for proxy type
      - WPAD - [http://wpad/wpad.dat](https://searchfox.org/mozilla-central/rev/d7a8eadc28298c31381119cbf25c8ba14b8712b3/netwerk/base/nsPACMan.cpp#37)
  - Extension APIs can set the proxy
  - Network change listeners:
    - Notifies Necko about various system IP related changes
  - Do we bypass proxy configuration?
    - Unix no proxy for [source](https://searchfox.org/mozilla-central/source/toolkit/system/unixproxy/nsUnixSystemProxySettings.cpp#172)
    - `CanUseProxy` function gets called [source](https://searchfox.org/mozilla-central/rev/d7a8eadc28298c31381119cbf25c8ba14b8712b3/netwerk/base/nsProtocolProxyService.cpp#1089)
  - Does the webext API also intercept SystemPrincipalRequests?
  - Are there any special requests which we don't tunnel through proxies?
    - [source](https://searchfox.org/mozilla-central/rev/d7a8eadc28298c31381119cbf25c8ba14b8712b3/docshell/base/nsIWebNavigation.idl#172) 
    - [source](https://searchfox.org/mozilla-central/rev/d7a8eadc28298c31381119cbf25c8ba14b8712b3/netwerk/protocol/http/nsIHttpChannelInternal.idl#273)
  - Network partitioning uses proxy in the hash key
    - [source](https://searchfox.org/mozilla-central/rev/d7a8eadc28298c31381119cbf25c8ba14b8712b3/netwerk/protocol/http/nsHttpConnectionInfo.cpp#131-132,168,170,197,199,201,204)
- **Operational Overview**
  - Steps followed while fetching a resource without proxy
    1. Listener opens a channel with a URL
    2. We get the IP address for the URL using DNS/DoH
    3. We make socket connections (TLS) to the IP address
    4. We send a HTTP request (GET) to the server
  - How do the above steps differ when using a proxy?
    1. Listener opens a channel with a URL
    2. Decide whether we need to use Proxy for URL using AsyncResolve
    3. Check async if we need proxy
    4. If we have a proxy connection, we directly connect to the proxy
    5. If no existing connection: We send the CONNECT method to the URL (only if it is HTTPS)
    6. We now have a byte tunnel to the URL
    7. We make socket connections (TLS) to the IP address
    8. We send a HTTP request (GET) to the server
  - Possible permutations of secure connections:
    - CLIENT -> PROXY -> SERVER HTTP Method
      - HTTP HTTP GET
      - HTTP HTTPS CONNECT
      - HTTPS HTTP GET
      - HTTPS HTTPS CONNECT
- **High-level code Proxy walkthrough**
  - SOCKS Protocol v/s HTTP proxy
    - [source](https://ma.ttias.be/socks-proxy-linux-ssh-bypass-content-filters/)
    - [Mitmproxy](https://mitmproxy.org/)
    - [Wireshark TLS](https://wiki.wireshark.org/TLS#Using_the_.28Pre.29-Master-Secret)
  - Proxies for reproducing Issues?
    - [Mitmproxy](https://mitmproxy.org/)
    - [Foxyproxy](https://addons.mozilla.org/en-US/firefox/addon/foxyproxy-standard/)
  - [Bugzilla: 621429](https://bugzilla.mozilla.org/show_bug.cgi?id=621429)
- **Process to release high-risk features**

## Aug 3, 2023

- **Security in Necko**
  - What are the various security checks done in Necko?
    - `doContentSecurityCheck`
	      - CSP policy checking during AsyncOpen()
	      - Called in both parent and child
	      - We need in both places because some information is available only in either child or parent
	      - Checks are done in Child to fail early
	      - Can’t trust the content process hence it is done in the parent as well
	      - Content process more vulnerable because it is running the JS
	      - [ROP](https://en.wikipedia.org/wiki/Return-oriented_programming)
	      - [Mozilla Security Sandbox Process Model](https://wiki.mozilla.org/Security/Sandbox/Process_model)
	      - [Firefox Update brings a whole new sort of security sandbox](https://nakedsecurity.sophos.com/2021/12/07/firefox-update-brings-a-whole-new-sort-of-security-sandbox/)
	    - CP Sandbox is configured in the OS 
	    - In general data coming from the content process must be validated
	    - Port related checks
    - CORS preflight
    - When does it get opened?

- **Bug Deep dives**
  - Discuss an interesting bug that you solved that might be helpful to others
  - Let's collaborate to brainstorm a solution for this bug.
  - Bug 479038 
    - How do I know if the URI being loaded is from an iframe source?
      - Page B is an iframe element in Page A
      - While loading Page B I need to know if this was from a frame source. 
      - With normal iframe from page we can get this from content policy in loadinfo: `nsIContentPolicy::TYPE_SUBDOCUMENT` or `nsIContentPolicy::TYPE_INTERNAL_FRAME`.
      - But if it is added from a script, the content policy from loadinfo does not contain this information.
    - Difference between referrer info 
      - Referrer info - for page that initiated the request 
        - (referrer headers?)
        - Info about the uri that has referred the page uri
        - [MDN - Referer](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Referer)
    - Review patch together

## July 20, 2023

- How does Devtools interact with Necko?
  - Devtool usually in Parentprocess??
  - Observers are registered 
  - We [source](https://searchfox.org/mozilla-central/rev/8d43262674d6c6d469b821cca579b1240ebb42a5/netwerk/protocol/http/nsIHttpProtocolHandler.idl#136-213)
- Http-activity distributor
  - Notifications are sent from http transactions
  - Transaction -> Distributor -> Listener
- Http Response Header
  - [source](https://searchfox.org/mozilla-central/rev/8d43262674d6c6d469b821cca579b1240ebb42a5/netwerk/protocol/http/nsHttpTransaction.cpp#2491)
- Throttler channel 
  - Throttles the network speed. For simulating network traffic speed. 
  - [source](https://searchfox.org/mozilla-central/rev/8d43262674d6c6d469b821cca579b1240ebb42a5/netwerk/protocol/http/nsHttpTransaction.cpp#329)
- Contact Points:
  - [Devtools Mozilla Source Docs](https://firefox-source-docs.mozilla.org/mots/index.html#devtools)
  - Honza, Hubert
- Ideas use the Professional Development budget?
  - Interesting soft skills workshops by Stanford
  - Perf.Now [conference in Amsterdam (Nov 2-3)](https://perfnow.nl/)
- Lots of interesting things to do and see in Quebec ;) - Thanks Andrew!
  - [Atlas Obscura Quebec](https://www.atlasobscura.com/things-to-do/quebec/places?page=1)

## July 13, 2023

- Redirection walkthrough
  - Sunil has doc - <link when ready>
  - “Internal redirection” - client side change (channel)
 .    - Old channel creates new
    - Auth stripping for cross-origin
    - Pass loadInfo
    - Copy Early hints observer
    - Listener is copied
    - notification callbacks too
    - Ex. webextension needs load info
- Channel is suspended while we are waiting for listeners
    - What happens on redirect failure (listener verification)
    - New channel OnStart/OnStop
    - Cancel Old Channel 
- Is WebExtension API to Necko different from that of DOM API? 
  - WebExtension API can cancel the channel
  - For DOM see webidl
  - See mdn page for more details

## July 6, 2023

Went through our current Open Questions:

1. How do we map a nsHttpChannel request to a tcp connections?
   - Http1: many to one with connection reuse, maybe not at the same time
   - Http2: many to one, using single tcp connection 
   - Http3: same, channels use same (UDP) connection
   - Hash key to ConnectionEntry has private, container, partition difference, all which will create different connections
2. What additional functionality is offered by the connection manager?
   - Timeout connections
   - Active connection and Idle connections
4. How does transaction handling differ between http1.1, http2 and http/3?
   - Probably handled by the remainder of Kershaw’s recent lightning talk
5. In which Process/threads does the HttpChannelChild, HttpChannelParent, HttpBackgroundChannelParent, HttpBackgroundChannelChild code run?
6. Is the main purpose of HttpBackgroundChannels to support ODT  for OMT?
   - Support IPC between httpchannelParent in the main process.
7. Retry logic for Connections??
   - Skip for now
8. When are transactions recycled?
   - It was noticed that transactions (memory addresses) seem to be re-used
   - This is probably the memory allocator just using the memory for a different transaction
   - Active to idle after timeout they are dropped. 
9. Where does the OnStartR and OnStopR reside. Main thread of parent process or main thread of content process? 
   - In Content process
	
10. Who calls nsHttpChannel::Connect?
    - Internal call
    - [Calls to nsHttpChannel::DoConnect](https://searchfox.org/mozilla-central/query/default?q=calls-to%3A%27mozilla%3A%3Anet%3A%3AnsHttpChannel%3A%3ADoConnect%27%20depth%3A4)

11. What is rate pacing?
    - [Bugzilla Reference](https://bugzilla.mozilla.org/show_bug.cgi?id=819734)
    - Traffic smoothing to reduce networking “bursting” to avoid packet loss
    - Buffer bloat
    - Say large file upload
    - Network buffers have many packets
    - Other ssh connection is queued

12. What is sticky connection
    - Sticky connection is “special” -> Connection based authentication (NTLM)
    - Auth retry request, same request with different transaction

We also went though “new necko story” components and “our users”.
[Google Doc Link](https://docs.google.com/document/d/17D4gR-DpaWyt7cJerUJSiSJICUY1EaEIRBPwvXR6xEU/edit#heading=h.8fn7ouivsx4g)


## June 29, 2023

- MOZ_LOGs from mochi/shell tests on try?
  - Example: `./mach try fuzzy --rebuild 20 --env "MOZ_LOG=nsHttp:5,EarlyHint:5" netwerk/test/browser/browser_103_*`
- Options on try to set environment variables
  - There is a way to retrigger with new env variables
    - Example?
- Custom push action in dropdown
  - #build or #sheriffs may know details
  - [Link](https://treeherder.mozilla.org/jobs?repo=try&revision=cd38eb2e6b9222742abeef34f8520258e6becf18&selectedTaskRun=GnKXaDusT82QJ-wc4wsCZw.0)
  - Looks like a bug
- Is there a way to trigger wpt and browser tests at the same time with try fuzzy?
  - (Triggering job will cause wpt to be run in wrong env)
  - This should work
- Pernosco
  - Add `--pernosco` to your `./mach try` (roughly speaking)
  - There is a way also from web UI
    - Click failing job > On bottom panel: Artifacts and debugging > “Reproduce this failure from pernosco”
- What do you all usually test using the try server?
  - Run Perf tests
    - `./mach try perf`
    - [Perfherder Comparison](https://treeherder.mozilla.org/perfherder/compare?originalProject=try&originalRevision=4cf3adb584ace59afaba83e88f8731ad3bc2351f&newProject=try&newRevision=afe66f2977b6ceab37d17a7a2abba7e1e818946a&framework=13&page=1)
  - How do I get conclusive results?
    - 10/10 is good amount of runs
    - Significant deltas are highlighted
    - `./mach try –android` (android is usually disabled by default)
- Run wide range of tests for my changes
  - Not for sec bugs (or at least be very cautious, nothing that would make it obvious what the security issue is)
    - If you must: Use innocuous commit message and don’t reference the bug number
    - [Security Bug Fixing Process](https://firefox-source-docs.mozilla.org/bug-mgmt/processes/fixing-security-bugs.html)
  - Checking all platforms (esp android)
  - Clang checks
  - Changes with large downstream dependents like Necko’s socket array (which touches every test)
    - `./mach try auto`
    - ??
- Try / Treeherder instance on local machine?
  - Docker image?
    - Probably non-trivial
    - Talk to team responsible (probably they do local stuff)

## June 23, 2023

- Intro to the meeting for new joiners
- Kershaw - [tips for analyzing HTTP logging](https://docs.google.com/presentation/d/1o_hX4QwWEgZP9QQfY9kfnZClFvPfVpu26P7HNh2tYJM/edit)

- Intercepted channel is only for Service workers
  - [Link to source](https://searchfox.org/mozilla-central/rev/d307d4d9f06dab6d16e963a4318e5e8ff4899141/netwerk/ipc/DocumentLoadListener.cpp#2634-2638)
- Channel suspension
- URLClassifier
- Webextensions
  - Can suspend or cancel a channel
- Main document load for channels for new content processes
- Logan
  - Select nsHttpChannel and state
  - Dummy channels for
    - Proxy resolution
    - Speculative connection
  - Stack trace with profiler
- Future Ideas:
  - Backtrack tool for tracing
    - [Backtrack meets Gecko Profiler](https://www.janbambas.cz/backtrack-meets-gecko-profiler/)
  - Improved logging in nsHttpChannel
  - Improving visibility of objects behind COMPtr
  - “Who is listener?”

## June 15, 2023

- TryDispatchTransaction, starting with step 4
- MakeNewConnection
  - create DNS and connect socket
    - `CreateDnsAndConnectSocket`
      - creates `DnsAndConnectSocket::DnsAndConnectSocket` object
      - Fires observation notifications
        - primary and backup
        - Backup seems to use same resolver, just runs if primary doesn’t finish on time
        - Probably because DNS is UDP based
      - Duplicate DNS resolution
    - `DnsAndConnectSocket` object is initialized
    - Has a statemachine for various states of DNS resolution and socket connection.
    - Checks for proxy connection
    - Connection is established through various callbacks with `SetupEvent`
    - Receives listener notifications via `nsITimerCallback`, `nsIDNSListener` which generates events to drive the state machine
    - Study Various callbacks
    - Only run with if don’t already have DNSAndConnectSocketOrTLS: [link](https://searchfox.org/mozilla-central/rev/1d43d9f3d0ffcbdb619cfd1e2911fb22d1456657/netwerk/protocol/http/nsHttpConnectionMgr.cpp#1000)
- Including wider team in this meeting
  - For inclusivity, but we also want to respect others’ time and provide opportunity for us to build our own muscle/independence
  - Additional meeting or add others as optional?
  - Decision: Add others as optional

## Jun 9, 2023

- Agreed on format for next time (topic: what happens to transaction after Init() ) 
- Sticky connection
- Multiple resources, websockets, (upgrade?)
- What happens to nsHttpTransaction after Init()?
  - Init() was called from nsHttpChannel::DoConnectActual() -> SetupTransaction(). So SetupTransaction() is basically done after nsHttpTransaction::Init() finishes. 
  - So DoConnectActual() then initiates the transaction :
    - nsHttpHandler::InitiateTransaction() -> nsHttpConnectionMgr::AddTransaction()
    - AddTransaction() passes the transaction across the thread boundary with PostEvent to OnMsgNewTransaction 
    - OnMsgNewTransaction() calls ProcessNewTransaction()
    - ProcessNewTransaction() will attempt to dispatch the transaction
    - TryDispatchTransaction
      - Tries to dispatch a transaction to a connection
      - Creates a new connection if necessary
    - We will discuss the details of this function next time.
  - If connections are full 
    - we return error MakeNewConnection and TryDispatchTransaction
    - and queue the transaction in the appropriate connection entry when there are no connections that can be immediately used. 
		  - What are some example cases where we queue?
		  - Why is there a pending queue for each connection entry?
		  - TCP head-of-line blocking?
	  - We will later pull of the queue
  - But how do we trigger further processing?
    - In Http/1.1 -> by restarting the transaction , which is triggered by closing transactions with certain settings
    - Examples?
- Connection Table (mCT) -> Hashmap of hashkey to connectionEntry
  - Hashkey is generated from the connectionInfo
- ConnectionEntry 
  - ConnectionEntry is mapping to the hash key of a connection info. A single origin can have different partition key, so we could have more than one connection entry to the same origin. For example, if you open example.com in different containers, we create a connection for each container tab.
  - Http/1.1 -> One to many mapping of connections
  - Http/2 -> One to one with connection
  - Each connection is backed by it own TCP socket
  - Each connection has a a few places for sockets 
  - But spdy connection is initialized with mSocketTransport
  - And mWebsocketHttp2Session is only used by websocket “fake” connection as pointer to the real session
  - So it looks like these are all backed by the same socket
  - The only thing I’m not sure of is the mProxyConnectStream. It is used when we try to send connect for proxy tunnel setup and so I think it is just here for convenience and similarly backed by the mSocketTransport.


## Jun 2, 2023

- Everyone agrees we will try to use draw.io in FSD
- Instead of mermaid, which is hard to maintain a GROWING doc
- Diff btw ConnectionMgr and ConnectionMgrShell?
- ConnectionMgrShell is interface for chrome (parent) process
- Socket thread on content process 
- Talks to background thread on parent process for the sole purpose of relaying info between parent’s network-socket-thread
- AltSvC? 
- Way to direct client to other server locations (like HTTP/3 for ex)
- Transaction setup
	- Transaction setup in nsHttpChannel, sometime after asyncOpen
	- Proxy uses CONNECT
	- What is notification callbacks used for? How related to observers?
	- NS_HTTP_STICKY_CONNECTION
	- For keeping connections around after transaction closed/reused
	- Websockets and upgrades
	- ConnectionInfo created in BeginConnect()
	- During setting up of transaction SetUpTransaction =>  request headers, flags related to transaction are set
	- Init() : 
	  - report the request header to devtools
	  - Http transaction headers are buffered to be sent on the wire
	- HTTPS RR 
	- Setup webtransport session event listener
- Agreed upon format for next time (see June 9)

## May 25, 2023

- Digitized page-load-to-connectionMgr drawing
- Expanded ConnectionMgr component
- Flow starts from chrome URL
- Generated some questions
- Looked at ConnectionEntry and ConnectionInfo
