"""
Generates curated (hand-modeled, not randomly sampled) reference tables:
  - integration_error_catalog.csv   : common SAP integration error signatures + resolutions
  - integration_patterns_catalog.csv: common enterprise integration patterns used with SAP
These are "knowledge base" style tables -- one row per distinct, realistic scenario,
useful for classification / NLP / RAG-style ML tasks.
"""
import pandas as pd
import itertools

OUT = "data"

# ---------------------------------------------------------------- error catalog
# Structure: (integration_type, error_code, short_description, likely_cause, resolution_steps, severity, typical_system)
error_catalog = [
    ("IDoc", "51", "Application document not posted",
     "Data inconsistency in target application (e.g. missing customer/material master record)",
     "Check IDoc segment data in WE02/WE05; verify referenced master data exists; reprocess via BD87",
     "High", "ECC / S4HANA"),
    ("IDoc", "56", "IDoc with errors added",
     "Syntax or structural error while adding the IDoc to the database",
     "Review IDoc control record and segment structure against the message type definition; check partner profile (WE20)",
     "Medium", "ECC / S4HANA"),
    ("IDoc", "64", "IDoc ready to be transferred to application",
     "Not an error state, but IDocs stuck here indicate the inbound processing job did not run",
     "Check background job scheduling for RBDAPP01 / workflow; verify inbound processing is not deactivated in WE20",
     "Medium", "ECC / S4HANA"),
    ("IDoc", "68", "Error - no further processing",
     "A custom exit or user-status routine explicitly stopped processing",
     "Debug the associated function module / process code in WE42; check custom Z-exits",
     "High", "ECC / S4HANA"),
    ("IDoc", "29", "Error in ALE service",
     "Distribution model (BD64) misconfigured or filter object excluding the record",
     "Review distribution model and filter/segment filters; regenerate partner profiles",
     "Medium", "ECC / S4HANA"),
    ("IDoc", "26", "Error during syntax check of IDoc (outbound)",
     "IDoc structure does not match the basic type definition (missing mandatory segment)",
     "Compare IDoc type (WE30) against generated data; check segment release/version",
     "High", "ECC / S4HANA"),
    ("IDoc", "20", "Error passing data to port",
     "Communication channel (RFC destination / file port) unreachable or misconfigured",
     "Test RFC destination in SM59; verify port definition in WE21; check target system availability",
     "Critical", "ECC / S4HANA"),
    ("IDoc", "02", "Error passing data to port (outbound, dispatch)",
     "tRFC queue stuck or destination system down at dispatch time",
     "Check tRFC monitor (SM58); reprocess stuck LUWs; confirm target availability",
     "Critical", "ECC / S4HANA"),
    ("IDoc", "Duplicate", "Duplicate IDoc detected for same business document",
     "Sender retried after a timeout without receiving acknowledgment, or interface lacks idempotency key",
     "Implement duplicate-check logic on the natural key (PO/order number) before posting; enable IDoc duplicate check in partner profile",
     "Medium", "PI/PO / CPI"),
    ("BAPI", "E-100", "BAPI_RETURN type E - mandatory field missing",
     "Calling program did not populate a required structure field",
     "Inspect BAPI_RETURN table for field name; validate mapping populates all mandatory fields before BAPI call",
     "Medium", "ECC / S4HANA"),
    ("BAPI", "E-101", "BAPI_RETURN type E - authorization missing",
     "Communication user lacks authorization object for the target transaction",
     "Add missing authorization object/values to the communication user's role via SU53 trace",
     "High", "ECC / S4HANA"),
    ("BAPI", "E-102", "BAPI commit not executed / changes rolled back",
     "Caller invoked the BAPI but never called BAPI_TRANSACTION_COMMIT",
     "Ensure orchestration layer explicitly commits after a successful BAPI call sequence",
     "High", "Middleware / Custom ABAP"),
    ("BAPI", "E-103", "Duplicate document number in BAPI create",
     "Number range buffer exhausted or external number assignment reused",
     "Check number range object (SNRO); switch to internal assignment or extend buffer",
     "Medium", "ECC / S4HANA"),
    ("RFC", "RFC_ERROR_SYSTEM_FAILURE", "Target system unreachable",
     "SAP Gateway/application server down, or network path blocked",
     "Check ST22/SM21 on target; validate network route and firewall rules; verify RFC destination load balancing",
     "Critical", "Any ABAP stack"),
    ("RFC", "RFC_ERROR_COMMUNICATION", "Connection to partner broke down",
     "TCP session dropped mid-call, often due to timeout or gateway restart",
     "Increase RFC timeout parameter; check SAP Gateway logs (dev_rfc.trc); enable retry with backoff",
     "High", "Any ABAP stack"),
    ("RFC", "RFC_ERROR_LOGON_FAILURE", "Logon failure calling remote system",
     "Expired password, locked user, or incorrect client/system number in RFC destination",
     "Reset service user credentials; verify RFC destination (SM59) client/system parameters",
     "High", "Any ABAP stack"),
    ("RFC", "SYSTEM_FAILURE", "Short dump in remote-enabled function module",
     "Unhandled exception in custom RFC-enabled FM logic",
     "Analyze ST22 short dump; add explicit exception handling in the function module",
     "High", "Custom ABAP"),
    ("OData", "400", "Bad Request - malformed payload",
     "Client sent a payload that does not match the OData service's EDM metadata",
     "Validate payload against $metadata; check for missing navigation properties or type mismatches",
     "Medium", "S4HANA / BTP Integration Suite"),
    ("OData", "401", "Unauthorized",
     "Missing or expired OAuth token / basic-auth credentials",
     "Refresh OAuth token; verify communication arrangement and communication system credentials",
     "High", "S4HANA / BTP Integration Suite"),
    ("OData", "403", "Forbidden - CSRF token missing",
     "Write operation (POST/PUT) sent without a valid X-CSRF-Token header",
     "Fetch CSRF token via GET with X-CSRF-Token: Fetch header before the write call",
     "Medium", "S4HANA OData"),
    ("OData", "404", "Entity not found",
     "Incorrect entity set name or key value in the request URL",
     "Confirm entity set name against service metadata; validate key encoding (special characters)",
     "Low", "S4HANA OData"),
    ("OData", "409", "Conflict - concurrent modification",
     "ETag mismatch; the entity was updated by another process since it was last read",
     "Re-fetch the entity to get the current ETag before retrying the update (optimistic concurrency)",
     "Medium", "S4HANA OData"),
    ("OData", "429", "Too Many Requests - throttled",
     "Client exceeded the tenant's configured rate limit",
     "Implement exponential backoff and request batching; review BTP service plan rate limits",
     "Medium", "BTP Integration Suite"),
    ("EDI", "997", "Functional Acknowledgment rejects transaction set",
     "Segment/element failed EDI standard or trading-partner-specific validation",
     "Review 997 AK3/AK4 loop for the failing segment/element; correct mapping and resend",
     "Medium", "EDI VAN / B2B Gateway"),
    ("EDI", "MAP-ERR", "Mapping engine transformation failure",
     "Source field value outside the expected code list for the target mapping (e.g. unknown UOM code)",
     "Extend the mapping's code-list lookup table; add default/error-queue handling for unmapped codes",
     "Medium", "SAP CPI / B2B Add-on"),
    ("CPI", "MPL-TIMEOUT", "Message Processing Log shows timeout",
     "Downstream HTTP receiver adapter exceeded configured timeout under load",
     "Increase receiver adapter timeout; check downstream system performance; consider async/queued pattern",
     "High", "SAP CPI"),
    ("CPI", "MPL-RETRY-EXHAUSTED", "Retry count exhausted, message failed",
     "Persistent downstream failure exceeded the configured number of automatic retries",
     "Investigate root cause in downstream system; use Message Processing Log manual resend after fix",
     "Critical", "SAP CPI"),
]

df_errors = pd.DataFrame(error_catalog, columns=[
    "INTEGRATION_TYPE", "ERROR_CODE", "SHORT_DESCRIPTION", "LIKELY_CAUSE",
    "RESOLUTION_STEPS", "SEVERITY", "TYPICAL_SYSTEM"
])
df_errors.insert(0, "ERROR_ID", ["ERR-" + str(i + 1).zfill(4) for i in range(len(df_errors))])
df_errors.to_csv(f"{OUT}/integration_error_catalog.csv", index=False)

# ---------------------------------------------------------------- integration patterns catalog
patterns = [
    ("Master Data Distribution (ALE)", "IDoc", "Async", "Sync customer/material/vendor master across SAP systems",
     "SAP ALE (native)", "Filter object maintenance; segment version mismatches across releases"),
    ("Order-to-Cash IDoc Flow", "IDoc", "Async", "ORDERS/ORDRSP/DESADV/INVOIC exchange with EDI trading partners",
     "SAP PI/PO, SAP CPI, B2B VAN", "Partner-specific mapping variance; sequencing of DESADV before INVOIC"),
    ("Real-time Order Creation", "BAPI", "Sync", "External web/mobile front-end creates sales orders in real time",
     "Custom middleware, SAP CPI", "Transaction rollback handling; duplicate submission from client retries"),
    ("Batch Financial Posting", "BAPI", "Sync (batch-scheduled)", "Nightly bulk posting of GL/AP/AR documents from a sub-ledger system",
     "SAP Process Integration, custom ABAP report", "Number range contention; partial-batch failure recovery"),
    ("Remote Function Call Integration", "RFC", "Sync", "Direct system-to-system calls for lookups (credit check, ATP, pricing)",
     "SAP Gateway, custom RFC clients (JCo)", "Connection pool exhaustion; timeout tuning under peak load"),
    ("S/4HANA API for Cloud Apps", "OData", "Sync", "Cloud application reads/writes business objects via SAP API Business Hub services",
     "SAP BTP Integration Suite, direct OData consumption", "CSRF token handling; entity deep-insert limitations"),
    ("Event-Driven Notifications", "SAP Event Mesh / Webhook", "Async", "Publish business events (e.g. goods receipt) to subscriber microservices",
     "SAP Event Mesh, Kafka bridge", "At-least-once delivery requiring consumer idempotency"),
    ("EDI B2B Exchange", "EDI (X12/EDIFACT)", "Async", "Purchase orders, ASNs and invoices exchanged with trading partners",
     "SAP CPI B2B Add-on, third-party VAN (e.g. SPS Commerce)", "Functional acknowledgment SLAs; partner onboarding overhead"),
    ("Data Replication to Data Lake", "CDC / ODP", "Async (near real-time)", "Replicate SAP tables to a cloud data lake for analytics",
     "SAP Landscape Transformation (SLT), Operational Data Provisioning", "Delta queue backlog under high change volume"),
    ("Middleware Orchestration Hub", "Multi-protocol (IDoc/REST/SOAP)", "Mixed", "Central integration platform brokering between SAP and 20+ non-SAP systems",
     "MuleSoft, Dell Boomi, SAP CPI, webMethods", "Interface sprawl and inconsistent error-handling standards across flows"),
]
df_patterns = pd.DataFrame(patterns, columns=[
    "PATTERN_NAME", "TECHNOLOGY", "SYNC_ASYNC", "TYPICAL_USE_CASE",
    "MIDDLEWARE_EXAMPLES", "COMMON_CHALLENGES"
])
df_patterns.insert(0, "PATTERN_ID", ["PAT-" + str(i + 1).zfill(3) for i in range(len(df_patterns))])
df_patterns.to_csv(f"{OUT}/integration_patterns_catalog.csv", index=False)

print("integration_error_catalog:", df_errors.shape)
print("integration_patterns_catalog:", df_patterns.shape)
