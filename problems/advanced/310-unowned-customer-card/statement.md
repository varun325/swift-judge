The Swift book's example: a `Customer` optionally owns a `CreditCard`, and every card **must** have a customer — so the card's reference is `unowned let customer: Customer` (non-optional, non-owning).

 For each customer create the objects inside a scope, log `"<card number> belongs to <name>"` if they have a card (card numbers start at 1000 and increase by 1 per card), and let them deallocate — both classes log `"deinit <name|card number>"`. Return the log.
