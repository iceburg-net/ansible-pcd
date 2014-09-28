s3ql
####


s3ql is great for mounting object-based storage (think Amazon S3) as
a regular block storage-like mounted filesystem w/ some caveats
and tweaks underneath. IMO it's great for remote backups, as 
in theory, you never need to grow the parition size.

metadata is stored at the remote end to keep it performant and
workable -- meaning that you can't read the files/directories
from your remote provider, but will first need to mount the
filesystem using FUSE-based s3ql to see the contents. 

@todo RedHat-compat