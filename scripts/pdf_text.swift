import Foundation
import PDFKit
for filename in CommandLine.arguments.dropFirst() {
 let url=URL(fileURLWithPath:filename)
 guard let doc=PDFDocument(url:url) else {print("Cannot open \(filename)");continue}
 var text=""
 for i in 0..<doc.pageCount {text += "\nPAGE \(i+1)\n" + (doc.page(at:i)?.string ?? "")}
 try text.write(to:url.deletingPathExtension().appendingPathExtension("txt"),atomically:true,encoding:.utf8)
 print("PDF \(url.lastPathComponent): \(doc.pageCount) pages, \(text.count) characters")
}
