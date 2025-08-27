import json
import numpy as np

# مثال بسيط (تجربة Toy)
results = {
    "model": "SRDF-Toy",
    "iterations": 5,
    "loss": list(np.random.rand(5)),
    "accuracy": list(np.random.rand(5))
}

with open("output.json", "w") as f:
    json.dump(results, f, indent=4)

print("✅ Toy example finished. Results saved to output.json")
