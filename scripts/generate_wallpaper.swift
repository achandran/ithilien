// Run from the repository root; see extras/wallpapers/README.md.
import Foundation
import ImageIO

func require(_ condition: Bool, _ message: String) throws {
    if !condition { throw NSError(domain: "IthilienWallpaper", code: 1,
                                 userInfo: [NSLocalizedDescriptionKey: message]) }
}

let root = URL(fileURLWithPath: FileManager.default.currentDirectoryPath)
let directory = root.appendingPathComponent("extras/wallpapers")
let output = directory.appendingPathComponent("ithilien_dynamic_desktop.heic")
let temporary = directory.appendingPathComponent(".ithilien_dynamic_desktop.heic-\(UUID().uuidString)")
defer { try? FileManager.default.removeItem(at: temporary) }

do {
    let images = try ["dawn", "dusk"].map { variant -> CGImage in
        let url = directory.appendingPathComponent("ithilien_\(variant)_desktop_5120x2880.png")
        guard let source = CGImageSourceCreateWithURL(url as CFURL, nil),
              let image = CGImageSourceCreateImageAtIndex(source, 0, nil) else {
            throw NSError(domain: "IthilienWallpaper", code: 2,
                          userInfo: [NSLocalizedDescriptionKey: "Cannot read \(url.path)"])
        }
        try require(image.width == 5120 && image.height == 2880,
                    "\(variant) must be 5120 × 2880; no resampling is performed.")
        return image
    }
    let appearance = ["l": 0, "d": 1]
    let data = try PropertyListSerialization.data(fromPropertyList: appearance,
                                                  format: .binary, options: 0)
    let namespace = "http://ns.apple.com/namespace/1.0/" as CFString
    let prefix = "apple_desktop" as CFString
    let path = "apple_desktop:apr" as CFString
    let metadata = CGImageMetadataCreateMutable()
    try require(CGImageMetadataRegisterNamespaceForPrefix(metadata, namespace, prefix, nil),
                "Cannot register wallpaper metadata namespace.")
    guard let tag = CGImageMetadataTagCreate(namespace, prefix, "apr" as CFString,
                                             .string, data.base64EncodedString() as CFString),
          let destination = CGImageDestinationCreateWithURL(temporary as CFURL,
                                                            "public.heic" as CFString, 2, nil) else {
        throw NSError(domain: "IthilienWallpaper", code: 3,
                      userInfo: [NSLocalizedDescriptionKey: "Cannot create HEIC destination."])
    }
    try require(CGImageMetadataSetTagWithPath(metadata, nil, path, tag),
                "Cannot set appearance metadata.")
    let options = [kCGImageDestinationLossyCompressionQuality: 1.0] as CFDictionary
    CGImageDestinationAddImageAndMetadata(destination, images[0], metadata, options)
    CGImageDestinationAddImage(destination, images[1], options)
    try require(CGImageDestinationFinalize(destination), "HEIC encoding failed.")

    guard let result = CGImageSourceCreateWithURL(temporary as CFURL, nil) else {
        throw NSError(domain: "IthilienWallpaper", code: 4,
                      userInfo: [NSLocalizedDescriptionKey: "Cannot reopen HEIC."])
    }
    try require(CGImageSourceGetCount(result) == 2, "Expected two HEIC frames.")
    try require(CGImageSourceGetPrimaryImageIndex(result) == 0, "Expected Dawn as primary image.")
    for index in 0..<2 {
        guard let image = CGImageSourceCreateImageAtIndex(result, index, nil) else {
            throw NSError(domain: "IthilienWallpaper", code: 5,
                          userInfo: [NSLocalizedDescriptionKey: "Cannot decode frame \(index)."])
        }
        try require(image.width == 5120 && image.height == 2880, "Incorrect frame dimensions.")
    }
    guard let saved = CGImageSourceCopyMetadataAtIndex(result, 0, nil),
          let value = CGImageMetadataCopyStringValueWithPath(saved, nil, path),
          let decoded = Data(base64Encoded: value as String),
          let mapping = try PropertyListSerialization.propertyList(from: decoded, options: [],
                                                                    format: nil) as? [String: Int] else {
        throw NSError(domain: "IthilienWallpaper", code: 6,
                      userInfo: [NSLocalizedDescriptionKey: "Cannot decode appearance metadata."])
    }
    try require(mapping == appearance, "Incorrect light/dark frame mapping.")
    if FileManager.default.fileExists(atPath: output.path) {
        _ = try FileManager.default.replaceItemAt(output, withItemAt: temporary)
    } else {
        try FileManager.default.moveItem(at: temporary, to: output)
    }
    print("Generated \(output.path)")
    print("Verified: two 5120 × 2880 frames; Light = Dawn (0), Dark = Dusk (1).")
} catch {
    fputs("\(error.localizedDescription)\n", stderr)
    exit(1)
}
