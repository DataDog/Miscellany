# Manual Testing Strategy

Make sure to stop the agent before running these tests.

## Uptime File and Log

 - delete the uptime file
 - delete the uptime log
 - run the check
 - both timestamps in uptime file should be the same
 - wait at least downtime_threshold seconds
 - run the check, wait a few seconds, then run it again
 - the downtime log should still not exist (because the previous interval had a length of zero)
 - the timestamps in the uptime file should be a few seconds apart
 - wait at least downtime_threshold seconds
 - run the check
 - both timestamps in uptime file should be the same
 - the uptime log should now exist and contain the previous contents of the uptime file
 - run the check, wait a few seconds, then run it again
 - wait at least downtime_threshold seconds
 - run the check
 - the uptime log should now contain two entries
 - cat the uptime log
 - add the following entry to the start of the uptime log: `1 2`
 - run the check
 - cat the uptime log
 - the uptime log should be as it was before an entry was added manually
 - delete the uptime file
 - run the check

## Metrics

 - delete the uptime file
 - delete the uptime log
 - run the agent for one minute (the `date` command is useful for this)
 - stop the agent and wait at least downtime_threshold seconds
 - run the agent for one minute
 - stop the agent and run the check

## Host crash

 - delete the uptime file
 - delete the uptime log
 - in a VM, configure an agent to run the uptime check
 - ensure that the uptime check is running by check the uptime file
 - power off the VM (don't shut it down gracefully)
 - ensure that the uptime previous uptime information is now in the uptime log, and that the uptime check continues to run