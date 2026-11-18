# Dataset card · synthetic-v1

This tiny dataset was authored specifically for the course. It is fictional, not scraped, not government data, and not personal information. It is embedded in Day 1 and Day 2 and exported by Day 4. No dataset download is necessary.

## Public service directory

| Key | Value |
|---|---|
| `ar` | يمكنك متابعة حالة طلبك باستخدام رقم المرجع. |
| `en` | You can check your application status using its reference number. |

The mock recognizes these two exact questions and one clarification example: `كيف أتابع طلبي؟`, `How can I check my application status?`, `ساعدني`. It does not understand arbitrary language. Case/wording coverage is deliberately limited.

## Application records

| Synthetic reference | Synthetic owner | Synthetic status |
|---|---|---|
| REF-1001 | demo-user-1 | under_review |
| REF-1002 | demo-user-2 | approved |

`REF-9999` intentionally does not exist. The trusted session fixture is `demo-user-1`. Request references are identifiers, not proof of ownership. The tool compares the trusted session to the record owner before returning status. User input cannot set the session. Production authentication is outside scope.

`not_found` and `access_denied` are internal test codes. Both have the same outward answer; denied responses do not include `approved`. In a real service, avoid revealing record existence through messages, timing, logs, or diagnostics. This small demo is not a complete security implementation.

## Ticket contract

Exactly four fields: `service` (service_info/application_status/other), `city` (Riyadh/Jeddah/unknown), `request_id` (null or REF- plus four ASCII digits), and `needs_clarification` (Boolean). A missing reference for application_status must set clarification to true. Only Riyadh extraction is implemented; Jeddah is an allowed schema value, not a claim that every place-name input is parsed.

## Golden cases

C01–C10 are included in Day 3: Arabic FAQ, English FAQ, owned record, absent record, missing reference, out-of-scope service, another owner's record, instruction override attempt, blank input, malformed ticket. Ten passing fixtures show that these code paths work, not language quality or production readiness.

No real names, phone numbers, IDs, applications or ministry data should be added. All statuses and identities are examples. If you adapt the lab, use new synthetic examples and document the change.
