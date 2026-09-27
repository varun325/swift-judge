// Renders build/icon.png (1024×1024) for the app bundle: `swift scripts/make-icon.swift`
import AppKit

let size = 1024.0
let image = NSImage(size: NSSize(width: size, height: size))
image.lockFocus()

// Rounded-square background with a Swift-orange gradient (macOS icon grid inset).
let inset = 100.0
let rect = NSRect(x: inset, y: inset, width: size - 2 * inset, height: size - 2 * inset)
let background = NSBezierPath(roundedRect: rect, xRadius: 185, yRadius: 185)
NSGradient(starting: NSColor(red: 0.98, green: 0.45, blue: 0.24, alpha: 1),
           ending: NSColor(red: 0.90, green: 0.20, blue: 0.16, alpha: 1))!.draw(in: background, angle: -90)

// A "{ ✓ }" mark: code braces around a check — code that passes the judge.
let paragraph = NSMutableParagraphStyle()
paragraph.alignment = .center
let attributes: [NSAttributedString.Key: Any] = [
    .font: NSFont.monospacedSystemFont(ofSize: 360, weight: .bold),
    .foregroundColor: NSColor.white,
    .paragraphStyle: paragraph,
]
NSString(string: "{ }").draw(in: NSRect(x: inset, y: 300, width: rect.width, height: 440), withAttributes: attributes)
let check = NSBezierPath()
check.lineWidth = 64
check.lineCapStyle = .round
check.lineJoinStyle = .round
check.move(to: NSPoint(x: 432, y: 520))
check.line(to: NSPoint(x: 500, y: 450))
check.line(to: NSPoint(x: 612, y: 590))
NSColor.white.setStroke()
check.stroke()

image.unlockFocus()
let png = NSBitmapImageRep(data: image.tiffRepresentation!)!.representation(using: .png, properties: [:])!
try! png.write(to: URL(fileURLWithPath: "build/icon.png"))
print("wrote build/icon.png")
