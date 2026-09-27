struct Declined: Error {}

protocol PaymentService: Sendable { func charge(cents: Int) async throws -> String }
protocol Analytics: AnyObject { func track(_ event: String) }

@MainActor
final class CheckoutViewModel {
    private let payments: any PaymentService
    private let analytics: any Analytics
    private(set) var receipt: String?
    private(set) var errorMessage: String?

    init(payments: any PaymentService, analytics: any Analytics) {
        self.payments = payments
        self.analytics = analytics
    }

    func pay(cents: Int) async {
        guard cents > 0 else { analytics.track("invalid_amount"); return }
        do {
            receipt = try await payments.charge(cents: cents)
            analytics.track("paid")
        } catch {
            errorMessage = "Payment failed"
            analytics.track("payment_failed")
        }
    }
}

struct StubPayments: PaymentService {
    let shouldFail: Bool
    func charge(cents: Int) async throws -> String {
        if shouldFail { throw Declined() }
        return "rcpt-\(cents)"
    }
}

final class SpyAnalytics: Analytics {
    private(set) var events: [String] = []
    func track(_ event: String) { events.append(event) }
}

@MainActor func runTests() async -> [String] {
    var results: [String] = []
    do {
        let spy = SpyAnalytics()
        let vm = CheckoutViewModel(payments: StubPayments(shouldFail: false), analytics: spy)
        await vm.pay(cents: 500)
        results.append("success: \(vm.receipt == "rcpt-500" && vm.errorMessage == nil && spy.events == ["paid"] ? "pass" : "fail")")
    }
    do {
        let spy = SpyAnalytics()
        let vm = CheckoutViewModel(payments: StubPayments(shouldFail: true), analytics: spy)
        await vm.pay(cents: 500)
        results.append("failure: \(vm.receipt == nil && vm.errorMessage != nil && spy.events == ["payment_failed"] ? "pass" : "fail")")
    }
    do {
        let spy = SpyAnalytics()
        let vm = CheckoutViewModel(payments: StubPayments(shouldFail: false), analytics: spy)
        await vm.pay(cents: 0)
        results.append("invalid: \(vm.receipt == nil && spy.events == ["invalid_amount"] ? "pass" : "fail")")
    }
    return results
}

func checkoutTests() async -> [String] {
    await runTests()
}
