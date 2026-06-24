"""Project package initialization.

This module includes a small monkey patch for a Django 4.2 / Python 3.14
compatibility bug in django.template.context.BaseContext.__copy__.
"""

import copy as _copy

from django.template.context import BaseContext


def _basecontext_copy(self):
	# Create a new uninitialized instance and copy relevant attributes.
	duplicate = object.__new__(type(self))

	# Shallow-copy other attributes so subclasses (Context, RequestContext)
	# keep attributes like 'template', 'render_context', etc.
	if hasattr(self, "__dict__"):
		for k, v in self.__dict__.items():
			if k == "dicts":
				continue
			try:
				setattr(duplicate, k, _copy.copy(v))
			except Exception:
				# Fallback: assign directly if copy fails
				setattr(duplicate, k, v)

	# Always copy the dicts list (the variable stack)
	duplicate.dicts = self.dicts[:]
	return duplicate


BaseContext.__copy__ = _basecontext_copy
