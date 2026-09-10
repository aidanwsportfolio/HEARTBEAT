# HEARTBEAT Project Overview

## Problem

Students at large universities depend on many digital services for coursework,
registration, housing, employment, campus involvement, and other daily needs.
When one of these services becomes unavailable or unreliable, students may not
immediately know whether the problem is affecting the university's service,
their network connection, their device, or only a subset of users.

At Louisiana State University, students use services such as Moodle, myLSU,
StarRez, Workday, eduroam, Navigate360, GROK, TigerLink, Persona, and SubItUp.
When problems occur, information often reaches students through word of mouth,
other students experiencing the same issue, or university communication such
as email. This can leave uncertainty during time-sensitive situations when a
student needs to know whether a service is working and what they should do next.

Students would benefit from a centralized way to quickly determine which
services appear operational or degraded, understand the scope and duration of
known problems, and find available alternatives or next steps.

## Proposed Solution

HEARTBEAT is a service-health monitoring platform designed to provide a
centralized view of the availability and performance of digital services.
The platform will help users determine whether a service appears operational,
degraded, or unavailable without requiring them to rely solely on word of
mouth or troubleshoot the issue independently.

HEARTBEAT will eventually combine automated service-health checks with
available incident information and user reports. Automated monitoring will
measure observable conditions such as service availability, response time,
and repeated failures. When an organization provides additional information,
HEARTBEAT can also communicate known incident details, expected restoration
times, affected services, and available alternatives.

Users will eventually be able to follow the services relevant to them and
receive notifications when meaningful changes occur, such that notifications
are personalized. This allows HEARTBEAT to provide useful service information 
without requiring users to receive alerts for every service monitored by an organization.

HEARTBEAT will distinguish between conditions it independently observes,
information officially provided by an organization or service provider, and
issues reported by users. The platform will not present an inferred cause,
restoration time, or scope as confirmed information when those details cannot
be independently determined.

## Initial Use Case: LSU HEARTBEAT

LSU HEARTBEAT will serve as the first implementation of the HEARTBEAT
platform. It will focus on monitoring digital services used by students at
Louisiana State University and provide a practical environment for developing
and testing HEARTBEAT's core monitoring capabilities.

The initial version will focus on a small set of web-accessible LSU services
rather than attempting to monitor every university system. Candidate services
include Moodle, myLSU, Workday, GROK, and TigerLink. Additional services can
be introduced as the platform's monitoring capabilities expand.

Some university resources require monitoring methods beyond a basic web
request. For example, determining whether eduroam is functioning for students
in a particular campus location cannot be reliably determined by a remote
HTTP health check. Authenticated applications may also appear reachable while
features behind the login page are unavailable.

For this reason, LSU HEARTBEAT will begin with conditions it can reasonably
observe and will expand to more complex service-health measurements as the
platform develops.
## Long-Term Vision

HEARTBEAT is intended to grow beyond its initial LSU implementation into a
reusable service-health monitoring platform for universities and other
organizations. Organizations could define the digital services relevant to
their communities while HEARTBEAT provides the underlying monitoring,
incident tracking, communication, and service-health infrastructure.

Future versions of HEARTBEAT could support personalized service subscriptions,
notifications, historical availability and performance data, incident
tracking, user-reported issues, and organization-provided incident updates.
These capabilities could allow users to understand both the current condition
of a service and its reliability over time.

As the platform grows, HEARTBEAT can also evolve technically to support
automated deployments, cloud infrastructure, containerized services,
observability, infrastructure as code, and distributed monitoring. These
technologies will be introduced when the scale and requirements of the system
create a need for them rather than being included solely for technical
complexity.

The initial implementation will remain intentionally limited in scope.
HEARTBEAT will first establish reliable core service monitoring through LSU
HEARTBEAT before expanding into a broader multi-organization platform.

## Project Goals

HEARTBEAT has the following primary goals:

1. Provide clear service-health visibility.
   Users should be able to quickly determine whether monitored services appear
   operational, degraded, or unavailable.

2. Produce reliable and transparent monitoring information.
   HEARTBEAT should distinguish between conditions it directly observes,
   information provided by organizations or service providers, and issues
   reported by users.

3. Improve communication during service disruptions.
   Users should eventually be able to receive relevant incident information,
   updates, alternatives, and notifications for the services they choose to
   follow.

4. Preserve service-health history.
   HEARTBEAT should eventually maintain historical availability, performance,
   and incident information so users and organizations can understand service
   reliability over time.

5. Support future expansion without requiring the initial implementation to
   solve every future use case.
   The core platform should avoid unnecessary assumptions specific to LSU while
   LSU HEARTBEAT remains the first and primary implementation.

6. Serve as a practical software engineering and infrastructure project.
   Development of HEARTBEAT should prioritize understanding the engineering
   problems behind each technical decision. New technologies should be
   introduced when they solve a requirement or limitation encountered as the
   system develops.

## Non-Goals

The initial development of HEARTBEAT will intentionally exclude several
capabilities that may become valuable as the platform matures. Limiting the
initial scope allows the project to establish reliable core monitoring before
introducing additional system complexity.

During the initial stages of development, HEARTBEAT will not attempt to:

- Monitor every digital service used by LSU.
- Determine the internal cause of an outage without authoritative information.
- Guarantee that a service is fully functional solely because it responds to
  an automated health check.
- Monitor location-dependent infrastructure such as campus Wi-Fi from a single
  remote monitoring system.
- Provide user accounts, personalized subscriptions, or notification delivery.
- Collect or incorporate user-submitted outage reports.
- Operate as a multi-organization production platform.
- Provide a native mobile application.
- Predict future outages using machine learning or artificial intelligence.

These capabilities may be considered in future versions when the core
monitoring system and project requirements create a clear need for them.
