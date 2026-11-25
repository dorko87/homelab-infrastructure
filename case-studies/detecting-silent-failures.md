# Detecting silent failures

A scheduled job can fail without producing a failure message. If it never starts, there may be no log entry or status change from the job itself.

This is a problem worth checking separately from service uptime. A running monitoring service does not mean that every scheduled task has run.

## The approach

The homelab documentation covers independent checks for missing scheduled activity, including dependency updates. Instead of relying only on the task to report errors, another check looks at whether expected activity has occurred recently enough.

A useful investigation starts by distinguishing three situations: a job that failed, a job that never started, and a job that ran but did not report its result. The checks and the evidence needed are different in each case.

## Example investigation

The following is a synthetic scenario, not a record of a specific outage.

Suppose a dependency update job has not reported activity within its expected interval. First check when it last ran, then check the scheduler and runner. If a run exists, inspect its result and confirm whether the reporting mechanism worked. If no run exists, investigate scheduling and execution before debugging the application itself.

An independent freshness check helps detect this situation even if the job is unable to send its own alert.

The public documentation does not establish measured detection times or a complete history of incidents.

See [observability](../reliability/observability.md).
