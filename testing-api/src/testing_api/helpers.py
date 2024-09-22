# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH

from tenacity import RetryError


class BetterRetryError(RetryError):
    def __str__(self) -> str:
        start = f"attempt_number={self.last_attempt.attempt_number}, "
        end = f"failed={self.last_attempt.failed}, done={self.last_attempt.done()}, cancelled={self.last_attempt.cancelled()}"

        if (exception := self.last_attempt.exception()) is not None:
            result = f"{start}exception={exception}, exception_type={type(exception)}"
        else:
            result = f"{start}result={self.last_attempt.result()}"

        return (result + end).replace("\n", "; ")
