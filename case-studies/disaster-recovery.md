# Planning backup and recovery

A successful backup job tells me that a copy was created. It does not tell me that an application can be restored from that copy.

## Backup design

The homelab backup inventory distinguishes covered, deferred and externally managed targets. Local and offsite copies serve different purposes. Offsite coverage is selective.

A backup on the same disk does not help if that disk fails. For databases, simply copying a live volume can also produce a copy that cannot be restored consistently. The documented approach includes database-native dumps alongside other backup data.

## What to check during a restore

A useful restore exercise would check that the expected backup exists, that the data can be read, that the application can start with the restored data, and that its key functions work.

These are verification steps, not a claim that every restore has already been tested. The current documentation does not establish universal restore coverage or measured recovery times.

See [backup and disaster recovery](../reliability/disaster-recovery.md) for the design.
