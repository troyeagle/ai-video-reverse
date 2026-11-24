import Foundation
import Vision
import AppKit

let directory = URL(fileURLWithPath: CommandLine.arguments[1])
let files = try FileManager.default.contentsOfDirectory(at: directory, includingPropertiesForKeys: nil).filter { $0.pathExtension == "png" }.sorted { $0.lastPathComponent < $1.lastPathComponent }
for file in files {
    print("\nFRAME \(file.lastPathComponent)")
    let request = VNRecognizeTextRequest()
    request.recognitionLevel = .accurate
    request.recognitionLanguages = ["zh-Hans", "en-US"]
    request.usesLanguageCorrection = true
    try VNImageRequestHandler(url: file).perform([request])
    for result in request.results ?? [] {
        if let text = result.topCandidates(1).first { print(text.string) }
    }
}
