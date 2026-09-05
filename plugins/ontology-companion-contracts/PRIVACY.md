# Privacy

Version 0.1.0 is a local application workflow. The publisher operates no hosted data service for it. Normal commands and local MCP do not make direct network requests, require an API key, upload artifacts, or invoke an external model.

Contracts reads the explicitly selected bounded JSON artifact or MCP argument and returns validation, compatibility, conversion or migration-plan results. It does not retain input artifacts in a registry or database. MCP conversion returns structured data; CLI conversion writes a new file only when an explicit output path is requested.

Source locators and supplied revisions remain data. The validator does not fetch referenced sources or verify external truth. Public examples and issue reports should use synthetic or non-sensitive data. Remove personal paths, credentials and private contents from diagnostics.

The user controls exported output files. Deleting an input or result does not remove copies from host transcripts, shell history, backups or independently shared artifacts.

Third-party hosts process prompts and tool results under their own terms. Installing this plugin does not change those host policies or give a cloud-only host access to the local computer.

[Security](SECURITY.md) · [Terms](TERMS.md) · [Support](SUPPORT.md)
