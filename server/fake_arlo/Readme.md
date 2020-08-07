# Fake Arlo client

We need to change the Arlo client to a fake one for integration
testing purposes because we can't use a real one. "Why?" you might
ask. We could... but Arlo seems to delete videos when the month
passes, so there's a high chance that we'd test with empty
arrays. Testing needs to make sure that data is available. Case in
point: without fake_arlo, if the library is empty, library syncing is
skipped and potential errors are never caught. Ideally, we would test
both cases (once with real and once with fake).

Of course, the challenge now is to keep the fake arlo client in sync
with the real arlo client (currently that is
[jeffreydwalter/arlo](https://github.com/jeffreydwalter/arlo)). This
would become the responsibility of this package (fake_arlo_client) to
test.

TODO: write tests to ensure fidelity of mocked data to real data. Not sure how
we'll do this tbh.