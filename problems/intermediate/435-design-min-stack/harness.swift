struct __Input: Decodable { let ops: [String]; let args: [[Int]] }

 func __run(_ __i: __Input) async throws -> [Int?] {
     var stack = MinStack()
     var out: [Int?] = []
     for (op, args) in zip(__i.ops, __i.args) {
         switch op {
         case "push": stack.push(args[0]); out.append(nil)
         case "pop": out.append(stack.pop())
         case "top": out.append(stack.top())
         default: out.append(stack.min())
         }
     }
     return out
 }
