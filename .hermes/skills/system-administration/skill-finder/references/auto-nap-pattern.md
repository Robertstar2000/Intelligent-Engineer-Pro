# auto_nap() Adaptive Cron Ticker

Pattern for an adaptive cron ticker that sleeps longer during idle periods.

See gateway/run.py `auto_nap()` function. Three modes:
- Normal: 60s ticks when user active within 10 min
- Idle: 30min ticks when no activity for 10+ min
- Reset: immediate return to 60s on any user input

Key: _record_cron_activity() called from _handle_message() for all non-internal events.
House-keeping uses wall-clock time (not tick counts) so cadences stay correct.
Requires gateway restart from shell to activate.
