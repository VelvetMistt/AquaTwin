from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
allow_origins=["http://localhost:5173", "http://localhost:5174"],    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "AquaTwin Backend is Running"
    }


@app.get("/simulate")
def simulate(
    tankLevel: float = 78,
    demandB: float = 10,
    pumpOn: bool = True,
    allocationA: float = 40,
    allocationB: float = 30,
    allocationC: float = 30
):
    if not pumpOn or tankLevel <= 0:
        return {
            "zoneA": {"flow": 0, "pressure": 0},
            "zoneB": {"flow": 0, "pressure": 0},
            "zoneC": {"flow": 0, "pressure": 0}
        }

    tankFactor = tankLevel / 78

    def calculate_zone(demand, allocation):
        baseCapacity = 7 * (allocation / 30)
        availableFlow = baseCapacity * tankFactor
        flow = min(demand, availableFlow)
        pressure = 3.2 * (flow / max(demand, 1))

        return {
            "flow": round(flow, 1),
            "pressure": round(pressure, 1)
        }

    return {
        "zoneA": calculate_zone(4, allocationA),
        "zoneB": calculate_zone(demandB, allocationB),
        "zoneC": calculate_zone(6, allocationC)
    }