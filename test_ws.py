from azure.quantum import Workspace

ws = Workspace(
    
resource_id="/subscriptions/81ff920d-3cb3-4d4e-bc42-417fbf947ba2/resourceGroups/quantum-rg/providers/Microsoft.Quantum/Workspaces/quantum-workspace-adry",
    location="northeurope"
)
print("Conectado al workspace ✅")
print("Targets disponibles:", [t.name for t in ws.get_targets()])

