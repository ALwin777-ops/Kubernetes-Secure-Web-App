# Kubernetes Pod Security Policy Test

## Objective
Verify that the Kubernetes Restricted Pod Security Standard
blocks pods with insecure container security settings.

## Test
Attempted to create a pod named `restricted-policy-test` with
`allowPrivilegeEscalation: true` and other missing security controls.

## Result
PASS - Kubernetes rejected the pod during admission.

## Policy violations reported
- `allowPrivilegeEscalation` was not false.
- Linux capabilities were not restricted by dropping ALL.
- Non-root execution was not required.
- An approved seccomp profile was not configured.

## Conclusion
The `secure-web` namespace enforces the Restricted Pod Security
Standard and blocks this test pod before creation.
