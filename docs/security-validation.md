# Kubernetes Secure Web App — Security Validation Report

## 1. Objective

Validate the security controls applied to a containerized web application deployed in a local Kubernetes cluster.

## 2. Test Results

| Test | Expected result | Observed result | Status |
|---|---|---|---|
| Health endpoint | Application reports healthy | Returned `healthy` | PASS |
| Application status | Application reports running | Returned `running` | PASS |
| Container identity | Runs without root privileges | UID 999, `appuser` | PASS |
| Root filesystem write | Write is blocked | `Read-only file system` error | PASS |
| Pod Security admission | Insecure pod is rejected | Kubernetes returned `Forbidden` | PASS |
| Rejected pod lookup | Test pod does not exist | Returned `NotFound` | PASS |

## 3. Container Hardening Controls

The Kubernetes deployment specifies:

- `runAsNonRoot: true`
- `runAsUser: 999`
- `runAsGroup: 999`
- `allowPrivilegeEscalation: false`
- `readOnlyRootFilesystem: true`
- Linux capabilities dropped using `drop: [ALL]`
- `seccompProfile.type: RuntimeDefault`
- CPU and memory requests and limits
- Startup, readiness, and liveness probes
- `automountServiceAccountToken: false`

These settings were confirmed in the deployment manifest. Runtime checks independently verified non-root execution and that writing to the root filesystem was blocked.

## 4. Kubernetes Pod Security Enforcement

The `secure-web` namespace was configured to enforce the Restricted Pod Security Standard.

A test pod was submitted with insecure settings. Kubernetes rejected it because it did not meet the requirements for privilege escalation, Linux capabilities, non-root execution, and seccomp.

A subsequent pod lookup returned `NotFound`, confirming the rejected test pod was not created.

## 5. Application Availability

The application remained operational after hardening:

- `GET /health` returned `healthy`.
- `GET /api/status` returned `running`.
- The pod was reported as ready with zero restarts in the collected output.

## 6. Limitations

This report documents the tests performed so far. It does not represent a complete penetration test, image vulnerability scan, network-policy validation, or proof that the application is free of vulnerabilities.

## 7. Conclusion

The collected evidence demonstrates successful application health checks, non-root execution, read-only root filesystem enforcement, and Kubernetes Restricted Pod Security admission enforcement in the local test environment.
