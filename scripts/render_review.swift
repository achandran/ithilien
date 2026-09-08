// Rasterize the review's drawing commands with one fixed font on macOS.
import AppKit
import CoreText
import Foundation
let input = URL(fileURLWithPath: CommandLine.arguments[1])
let output = URL(fileURLWithPath: CommandLine.arguments[2])
let data = try JSONSerialization.jsonObject(with: Data(contentsOf: input)) as! [String: Any]
let width = data["width"] as! Int, height = data["height"] as! Int
func color(_ hex: String) -> NSColor {
  let n = UInt32(hex.dropFirst(), radix: 16)!
  return NSColor(srgbRed: CGFloat((n >> 16) & 255)/255, green: CGFloat((n >> 8) & 255)/255, blue: CGFloat(n & 255)/255, alpha: 1)
}
let image = NSImage(size: NSSize(width: width, height: height))
image.lockFocusFlipped(true)
for c in data["commands"] as! [[String: Any]] {
  let x = c["x"] as! Double, y = c["y"] as! Double
  let ink = color(c["color"] as! String)
  if let text = c["text"] as? String {
    let style = c["style"] as? String ?? "regular"
    let fontName = style == "bold" ? "BerkeleyMono-Bold" : style == "italic" ? "BerkeleyMono-Oblique" : "BerkeleyMono-Regular"
    let fontURL = FileManager.default.homeDirectoryForCurrentUser.appendingPathComponent("Library/Fonts/\(fontName).otf")
    guard let provider = CGDataProvider(url: fontURL as CFURL), let cgFont = CGFont(provider) else { fatalError("Install Berkeley Mono for matched review rendering") }
    let font = CTFontCreateWithGraphicsFont(cgFont, 15, nil, nil) as NSFont
    (text as NSString).draw(at: NSPoint(x: x, y: y), withAttributes: [.font:font, .foregroundColor:ink])
  } else {
    ink.setFill()
    NSRect(x: x, y: y, width: c["w"] as! Double, height: c["h"] as! Double).fill()
  }
}
image.unlockFocus()
let bitmap = NSBitmapImageRep(data: image.tiffRepresentation!)!
try bitmap.representation(using: .png, properties: [:])!.write(to: output)
