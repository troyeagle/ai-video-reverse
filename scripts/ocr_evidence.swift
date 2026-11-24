import Foundation
import Vision

for arg in CommandLine.arguments.dropFirst() {
    let dir=URL(fileURLWithPath:arg)
    let files=try FileManager.default.contentsOfDirectory(at:dir,includingPropertiesForKeys:nil).filter{["jpg","png"].contains($0.pathExtension)}.sorted{$0.lastPathComponent<$1.lastPathComponent}
    var output:[[String:Any]]=[]
    for file in files {
        let request=VNRecognizeTextRequest()
        request.recognitionLevel = .accurate
        request.recognitionLanguages=["zh-Hans","en-US"]
        request.usesLanguageCorrection=true
        do {
            try VNImageRequestHandler(url:file).perform([request])
            let boxes=(request.results ?? []).compactMap { result -> [String:Any]? in
                guard let candidate=result.topCandidates(1).first else{return nil}
                let b=result.boundingBox
                return ["text":candidate.string,"confidence":candidate.confidence,"x":b.minX,"y":b.minY,"width":b.width,"height":b.height]
            }
            output.append(["frame":file.lastPathComponent,"time":Double(file.deletingPathExtension().lastPathComponent) ?? 0,"boxes":boxes])
        } catch { output.append(["frame":file.lastPathComponent,"error":String(describing:error)]) }
    }
    let data=try JSONSerialization.data(withJSONObject:output,options:[.prettyPrinted,.sortedKeys,.withoutEscapingSlashes])
    try data.write(to:dir.deletingLastPathComponent().appendingPathComponent("ocr.json"))
    print("OCR \(dir.path): \(output.count) frames")
}
