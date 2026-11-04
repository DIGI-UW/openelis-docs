#!/usr/bin/env python3
"""replace-att.py <pageId> <file>... : upload files as attachments (replacing same-named ones)."""
import sys, os, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("pub", os.path.join(HERE, "confluence-publish.py"))
pub = importlib.util.module_from_spec(spec); spec.loader.exec_module(pub)
base, auth = pub.load_creds()
pid = sys.argv[1]
ex = pub.existing_attachments(base, auth, pid)
for f in sys.argv[2:]: pub.upload_attachment(base, auth, pid, f, ex)
