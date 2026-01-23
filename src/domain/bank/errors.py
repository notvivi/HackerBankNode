class DomainError(Exception):
    """
    Base exception for domain-level errors.

    DomainError represents violations of business rules and
    invariants within the banking domain. It must be raised
    only from domain entities or domain services and should
    not depend on infrastructure or presentation concerns.

    Notes
    -----
    - DomainError signals a business rule violation, not a
      technical failure.
    - It should be handled at the application layer and
      translated into user-facing or transport-level errors.
    """
    pass

