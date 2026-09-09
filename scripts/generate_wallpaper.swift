import CoreGraphics
import Foundation
import ImageIO

let width = 6016
let height = 3760
// Read canonical palettes; never duplicate Day/Night colors in this generator.
let paletteDirectory = URL(fileURLWithPath: #filePath).deletingLastPathComponent().deletingLastPathComponent().appendingPathComponent("palette")
func canvas(_ variant: String) throws -> String {
  let data = try Data(contentsOf: paletteDirectory.appendingPathComponent("ithilien-\(variant).json"))
  let palette = try JSONSerialization.jsonObject(with: data) as! [String: Any]
  return (palette["backgrounds"] as! [String: String])["base"]!.replacingOccurrences(of: "#", with: "")
}
let dayHex = try canvas("day")
let nightHex = try canvas("night")

enum WallpaperError: Error, CustomStringConvertible {
  case invalidHex(String)
  case imageCreation
  case destinationCreation
  case finalization

  var description: String {
    switch self {
    case .invalidHex(let value): return "Invalid hex color: \(value)"
    case .imageCreation: return "Could not create wallpaper frame"
    case .destinationCreation: return "Could not create HEIC destination"
    case .finalization: return "Could not finalize HEIC output"
    }
  }
}

func colorComponents(_ hex: String) throws -> (CGFloat, CGFloat, CGFloat) {
  let clean = hex.trimmingCharacters(in: CharacterSet(charactersIn: "#"))
  guard clean.count == 6, let value = Int(clean, radix: 16) else {
    throw WallpaperError.invalidHex(hex)
  }
  return (
    CGFloat((value >> 16) & 0xff) / 255,
    CGFloat((value >> 8) & 0xff) / 255,
    CGFloat(value & 0xff) / 255
  )
}

func solidImage(hex: String) throws -> CGImage {
  let (red, green, blue) = try colorComponents(hex)
  guard
    let colorSpace = CGColorSpace(name: CGColorSpace.sRGB),
    let context = CGContext(
      data: nil,
      width: width,
      height: height,
      bitsPerComponent: 8,
      bytesPerRow: width * 4,
      space: colorSpace,
      bitmapInfo: CGImageAlphaInfo.noneSkipLast.rawValue
    )
  else { throw WallpaperError.imageCreation }

  context.setFillColor(red: red, green: green, blue: blue, alpha: 1)
  context.fill(CGRect(x: 0, y: 0, width: width, height: height))
  guard let image = context.makeImage() else { throw WallpaperError.imageCreation }
  return image
}

func appearanceMetadata() throws -> CGImageMetadata {
  let metadata = CGImageMetadataCreateMutable()
  CGImageMetadataRegisterNamespaceForPrefix(
    metadata,
    "http://ns.apple.com/namespace/1.0/" as CFString,
    "apple_desktop" as CFString,
    nil
  )
  let appearance = ["l": 0, "d": 1]
  let plist = try PropertyListSerialization.data(
    fromPropertyList: appearance,
    format: .binary,
    options: 0
  )
  let tag = CGImageMetadataTagCreate(
    "http://ns.apple.com/namespace/1.0/" as CFString,
    "apple_desktop" as CFString,
    "apr" as CFString,
    .string,
    plist.base64EncodedString() as CFString
  )!
  CGImageMetadataSetTagWithPath(metadata, nil, "apple_desktop:apr" as CFString, tag)
  return metadata
}

func generate(output: URL) throws {
  let day = try solidImage(hex: dayHex)
  let night = try solidImage(hex: nightHex)
  guard let destination = CGImageDestinationCreateWithURL(
    output as CFURL,
    "public.heic" as CFString,
    2,
    nil
  ) else { throw WallpaperError.destinationCreation }

  let options = [kCGImageDestinationLossyCompressionQuality: 1.0] as CFDictionary
  CGImageDestinationAddImageAndMetadata(destination, day, try appearanceMetadata(), options)
  CGImageDestinationAddImage(destination, night, options)
  guard CGImageDestinationFinalize(destination) else { throw WallpaperError.finalization }
}

func inspect(input: URL) throws {
  guard let source = CGImageSourceCreateWithURL(input as CFURL, nil) else {
    throw WallpaperError.destinationCreation
  }
  let count = CGImageSourceGetCount(source)
  let metadata = CGImageSourceCopyMetadataAtIndex(source, 0, nil)
  let tag = metadata.flatMap {
    CGImageMetadataCopyTagWithPath($0, nil, "apple_desktop:apr" as CFString)
  }
  let apr = tag.flatMap { CGImageMetadataTagCopyValue($0) as? String } ?? "missing"
  print("count=\(count)")
  print("size=\(width)x\(height)")
  print("day=#\(dayHex) frame=0")
  print("night=#\(nightHex) frame=1")
  print("apr=\(apr)")
}

do {
  let arguments = CommandLine.arguments
  guard arguments.count >= 3, ["generate", "inspect"].contains(arguments[1]) else {
    print("usage: generate_wallpaper generate|inspect OUTPUT.heic")
    exit(2)
  }
  let url = URL(fileURLWithPath: arguments[2])
  if arguments[1] == "generate" { try generate(output: url) }
  try inspect(input: url)
} catch {
  fputs("error: \(error)\n", stderr)
  exit(1)
}
