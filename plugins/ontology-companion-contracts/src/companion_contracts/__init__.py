"""Offline draft ontology interchange validation; no authorization or truth checks."""
from .validator import (
    CONTRACT_VERSION, CO_NAMESPACE, MAX_BYTES, compatibility, migration_plan,
    validate_artifact, validate_bytes, read_artifact,
)
from .code_adapter import PRODUCT_VERSION, convert_code_snapshot

__all__ = ["CONTRACT_VERSION", "CO_NAMESPACE", "MAX_BYTES", "compatibility",
           "migration_plan", "validate_artifact", "validate_bytes", "read_artifact",
           "PRODUCT_VERSION", "convert_code_snapshot"]
