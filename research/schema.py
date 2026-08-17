from enum import StrEnum

from pydantic import BaseModel, Field, HttpUrl


class AuthMethod(StrEnum):
    OAUTH2 = "OAuth2"
    API_KEY = "API key"
    BASIC = "Basic"
    TOKEN = "token"
    OTHER = "other"


class SelfServeStatus(StrEnum):
    SELF_SERVE_FREE = "self-serve-free"
    SELF_SERVE_TRIAL = "self-serve-trial"
    PAID_PLAN = "paid-plan"
    ADMIN_APPROVAL = "admin-approval"
    PARTNER_GATED = "partner-gated"


class ApiSurface(StrEnum):
    REST = "REST"
    GRAPHQL = "GraphQL"
    SOAP = "SOAP"
    SDK_ONLY = "SDK-only"
    NONE_PUBLIC = "none-public"


class ApiBreadth(StrEnum):
    NARROW = "narrow"
    MODERATE = "moderate"
    BROAD = "broad"


class HasMcp(StrEnum):
    YES_OFFICIAL = "yes-official"
    YES_COMMUNITY = "yes-community"
    NO = "no"


class Buildability(StrEnum):
    BUILDABLE_NOW = "buildable-now"
    BUILDABLE_WITH_FRICTION = "buildable-with-friction"
    BLOCKED = "blocked"


class _FindingFields(BaseModel):
    """Fields the research agent itself is responsible for determining."""

    one_liner: str

    auth_method: AuthMethod
    self_serve_status: SelfServeStatus
    api_surface: ApiSurface
    api_breadth: ApiBreadth
    has_mcp: HasMcp
    buildability: Buildability

    main_blocker: str = Field(
        description="Free text. Empty string if buildability is buildable-now."
    )
    evidence_url: HttpUrl = Field(
        description="A page the agent actually fetched, never a guessed URL."
    )
    confidence: float = Field(ge=0.0, le=1.0)


class AgentSubmission(_FindingFields):
    """Exact shape of the submit_finding tool-call arguments.

    A hallucinated enum value fails Pydantic validation at the tool-call
    boundary rather than silently becoming a guessed valid value.
    """


class Finding(_FindingFields):
    """One complete row: agent output plus the caller-injected identity
    fields (app/category), which the model never gets to invent."""

    app: str
    category: str
