// Native window discovery and sRGB screenshot inspection. No input synthesis.
import AppKit
import CoreGraphics
import Foundation
import Vision

func emit(_ value: Any) throws {
    let bytes = try JSONSerialization.data(withJSONObject: value, options: [.sortedKeys])
    print(String(data: bytes, encoding: .utf8)!)
}
let args = Array(CommandLine.arguments.dropFirst())
do {
    if args.first == "windows", args.count == 2 {
        guard CGPreflightScreenCaptureAccess() else {
            throw NSError(domain: "GhosttyCapture", code: 1, userInfo: [NSLocalizedDescriptionKey: "Screen Recording permission is unavailable"])
        }
        let windows = CGWindowListCopyWindowInfo([.optionOnScreenOnly, .excludeDesktopElements], kCGNullWindowID) as? [[String: Any]] ?? []
        let matches = windows.filter {
            ($0[kCGWindowOwnerName as String] as? String) == "Ghostty" &&
            ($0[kCGWindowName as String] as? String) == args[1] &&
            ($0[kCGWindowLayer as String] as? Int) == 0
        }.compactMap { $0[kCGWindowNumber as String] as? Int }
        try emit(["windows": matches])
    } else if args.first == "ocr-rows", args.count == 2 {
        let data = try Data(contentsOf: URL(fileURLWithPath: args[1]))
        let inputs = try JSONSerialization.jsonObject(with: data) as! [[String: Any]]
        var output: [[String: Any]] = []
        for input in inputs {
            let path = input["path"] as! String
            guard let image = NSImage(contentsOfFile: path),
                  let cg = image.cgImage(forProposedRect: nil, context: nil, hints: nil) else {
                throw NSError(domain: "GhosttyCapture", code: 2)
            }
            let request = VNRecognizeTextRequest()
            request.recognitionLevel = .accurate
            request.usesLanguageCorrection = false
            request.recognitionLanguages = ["en-US"]
            try VNImageRequestHandler(cgImage: cg).perform([request])
            let fragments = (request.results ?? []).sorted { $0.boundingBox.minX < $1.boundingBox.minX }.compactMap { item -> [String: Any]? in
                guard let text = item.topCandidates(1).first else { return nil }
                return ["text": text.string, "confidence": text.confidence]
            }
            output.append(["row": input["row"]!, "fragments": fragments])
        }
        try emit(["rows": output])
    } else if args.first == "ocr", args.count == 2 {
        guard let image = NSImage(contentsOfFile: args[1]),
              let cg = image.cgImage(forProposedRect: nil, context: nil, hints: nil) else {
            throw NSError(domain: "GhosttyCapture", code: 2)
        }
        let request = VNRecognizeTextRequest()
        request.recognitionLevel = .accurate
        request.usesLanguageCorrection = false
        request.recognitionLanguages = ["en-US"]
        try VNImageRequestHandler(cgImage: cg).perform([request])
        let lines = (request.results ?? []).compactMap { item -> [String: Any]? in
            guard let text = item.topCandidates(1).first else { return nil }
            let b = item.boundingBox
            return ["text": text.string, "confidence": text.confidence,
                    "box": [b.minX, b.minY, b.width, b.height]]
        }
        try emit(["lines": lines])
    } else if args.first == "pixels", args.count >= 3 {
        guard let image = NSImage(contentsOfFile: args[1]),
              let cg = image.cgImage(forProposedRect: nil, context: nil, hints: nil),
              let space = CGColorSpace(name: CGColorSpace.sRGB) else {
            throw NSError(domain: "GhosttyCapture", code: 2, userInfo: [NSLocalizedDescriptionKey: "Cannot decode screenshot"])
        }
        let width = cg.width, height = cg.height
        var pixels = [UInt8](repeating: 0, count: width * height * 4)
        let targets = args.dropFirst(2).map { value -> (String, Int, Int, Int) in
            let n = UInt32(value.dropFirst(), radix: 16)!
            return (value, Int((n >> 16) & 255), Int((n >> 8) & 255), Int(n & 255))
        }
        var counts = Dictionary(uniqueKeysWithValues: targets.map { ($0.0, 0) })
        try pixels.withUnsafeMutableBytes { data in
            guard let ctx = CGContext(data: data.baseAddress, width: width, height: height,
                                      bitsPerComponent: 8, bytesPerRow: width * 4, space: space,
                                      bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue | CGBitmapInfo.byteOrder32Big.rawValue) else {
                throw NSError(domain: "GhosttyCapture", code: 3)
            }
            ctx.draw(cg, in: CGRect(x: 0, y: 0, width: width, height: height))
            let buffer = data.bindMemory(to: UInt8.self)
            for i in stride(from: 0, to: buffer.count, by: 4) where buffer[i+3] == 255 {
                for (key, r, g, b) in targets where abs(Int(buffer[i])-r) <= 2 && abs(Int(buffer[i+1])-g) <= 2 && abs(Int(buffer[i+2])-b) <= 2 {
                    counts[key, default: 0] += 1
                }
            }
        }
        try emit(["width": width, "height": height, "color_space": "sRGB", "counts": counts])
    } else {
        throw NSError(domain: "GhosttyCapture", code: 4, userInfo: [NSLocalizedDescriptionKey: "Expected windows TITLE or pixels PNG HEX..."])
    }
} catch {
    fputs("\(error.localizedDescription)\n", stderr)
    exit(1)
}
