How to do necko triaging

Nick's Triage App

https://nwgh.github.io/necko-triage/

Bugzilla

  - UNTRIAGED bugs with no needinfo :  https://mzl.la/2oaZl1K
  - UNTRIAGED bugs: https://mzl.la/2wAv7XZ
  - MALFORMED bugs (have necko-triaged set but no priority): https://mzl.la/2xXf2jc
  - P1 bugs  https://mzl.la/2he1C85
  - P2 bugs  https://mzl.la/2yaD1aO
  - P3 bugs  (backlog) https://mzl.la/2xcYzEL
  - P5 bugs (would take): https://mzl.la/2hdnQXy

Priorities

- P1 bugs (Blocker: get someone assigned ASAP: also EMAIL necko@moz whenever we have a new P1 bug)
- P2 bugs (Active--we intend to work on these now or this quarter)
- P3 bugs (backlog)
- There is no P4--don't use it
- P5 bugs (would take)

Principles

- P1 bugs MUST have a person assigned
- Non-necko people can be assigned to necko bugs just fine
- Bugs filed by wpt-bot should be marked triaged as P5. If something is needed there, someone can ni? one of us.

Mark as triaged

- Set [necko-triaged] in the whiteboard for bugs that have been triaged.

- Note:
    - Android crashes on infra are currently not symbolicated: https://bugzilla.mozilla.org/show_bug.cgi?id=1389805 (makes triaging/diagnosing android crash bugs hard/impossible)

Discussion

- Incoming bugs with ongoing discussions and/or NI? Should we leave them without [necko-triaged] until some point? If so, at which point?
- Should we keep using ni?2018-MM-DD whiteboard keyword to mark bugs with pending ni on reporters or should we spilt the TRIAGE search query to those with and without ni? and go through them separately?

    I made a separate list. Maybe we should decide on a time period after which we should close bugs if reporters do not answer. 30 days?

        In the past during necko meetings, values ranging from 2-4 weeks have been mentioned. I think 1 month/30 days is a fine value (though on my grumpier days I'd argue for 2 weeks). Bugs should be marked RESOLVED/INCOMPLETE at that point.

    (Daniel) I vote on no-response in 30 days and without enough clarity means => RESOLVED/INCOMPLETE.

- (Daniel) On Networking bugs with non-necko people assigned, how do we handle Priority? It feels weird for me to set a prio for people outside of our work flow. Untriaged bugs that have someone assigned and have a patch/review pending, I set P1 (clearly work in progress). If assigned and no patch attached, maybe P2/P3 depending on how serious the problem seems.
     - (Nick) I've been setting them as P5 (would take) since that seems most reasonable. We're open to taking it, and someone else is working on it. Though I suppose if it gets abandoned, that could lead to issues with something we really want done but is now marked P5...

