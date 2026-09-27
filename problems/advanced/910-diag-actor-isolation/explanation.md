*actor-isolated property 'value' can not be referenced from a nonisolated context*. Outside the actor, access requires `await` (and therefore an async context) so the actor can serialise it.
