import subprocess
import json
from datetime import datetime

def run_kubectl(command):
    """Run kubectl command and return output"""
    try:
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True
        )
        return result.stdout + result.stderr
    except Exception as e:
        return str(e)

def get_cluster_logs():
    """Collect logs from all pods"""
    print("\n📊 Collecting cluster information...")
    
    pods = run_kubectl("kubectl get pods --all-namespaces")
    events = run_kubectl("kubectl get events --all-namespaces --sort-by='.lastTimestamp' | tail -20")
    nodes = run_kubectl("kubectl get nodes")
    
    return {
        "pods": pods,
        "events": events,
        "nodes": nodes,
        "timestamp": datetime.now().isoformat()
    }

def analyze_issues(cluster_data):
    """Analyze cluster data and identify issues"""
    print("\n🔍 Analyzing cluster issues...")
    
    issues = []
    recommendations = []
    scripts = []

    # Check for pending pods
    if "Pending" in cluster_data["pods"]:
        issues.append("❌ Pending pods detected")
        recommendations.append("Check node resources and pod scheduling")
        scripts.append("kubectl describe pods --field-selector=status.phase=Pending --all-namespaces")

    # Check for crashloopbackoff
    if "CrashLoopBackOff" in cluster_data["pods"]:
        issues.append("❌ CrashLoopBackOff detected")
        recommendations.append("Check pod logs for application errors")
        scripts.append("kubectl logs --previous <pod-name> -n <namespace>")

    # Check for failed pods
    if "Error" in cluster_data["pods"] or "Failed" in cluster_data["pods"]:
        issues.append("❌ Failed pods detected")
        recommendations.append("Restart failed deployments")
        scripts.append("kubectl rollout restart deployment --all-namespaces")

    # Check node status
    if "NotReady" in cluster_data["nodes"]:
        issues.append("❌ Node NotReady detected")
        recommendations.append("Check node health and kubelet status")
        scripts.append("kubectl describe node <node-name>")

    # All healthy
    if not issues:
        issues.append("✅ No critical issues detected")
        recommendations.append("Cluster is healthy - continue monitoring")

    return issues, recommendations, scripts

def generate_report(cluster_data, issues, recommendations, scripts):
    """Generate SRE report"""
    
    report = f"""
=====================================
🤖 AI AGENT - EKS OPERATIONS REPORT
=====================================
Timestamp: {cluster_data['timestamp']}
Cluster: fitness-tracker-cluster
Region: us-east-2

📋 CLUSTER STATUS:
{cluster_data['nodes']}

📦 POD STATUS:
{cluster_data['pods']}

🚨 ISSUES DETECTED:
"""
    for issue in issues:
        report += f"  {issue}\n"

    report += "\n💡 RECOMMENDATIONS:\n"
    for rec in recommendations:
        report += f"  → {rec}\n"

    report += "\n🔧 AUTOMATION SCRIPTS:\n"
    for script in scripts:
        report += f"  $ {script}\n"

    report += """
📈 RECENT EVENTS:
""" + cluster_data['events']

    report += """
=====================================
        SRE RUNBOOK
=====================================
1. Check pod status:
   $ kubectl get pods --all-namespaces

2. Check pod logs:
   $ kubectl logs <pod-name> -n <namespace>

3. Restart deployment:
   $ kubectl rollout restart deployment/<name>

4. Scale deployment:
   $ kubectl scale deployment/<name> --replicas=3

5. Check resource usage:
   $ kubectl top nodes
   $ kubectl top pods

6. Check events:
   $ kubectl get events --sort-by='.lastTimestamp'

7. Force delete stuck pod:
   $ kubectl delete pod <pod-name> --grace-period=0 --force
=====================================
"""
    return report

def main():
    print("🚀 Starting AI Agent for EKS Operations...")
    print("=" * 50)
    
    # Step 1 - Collect data
    cluster_data = get_cluster_logs()
    
    # Step 2 - Analyze
    issues, recommendations, scripts = analyze_issues(cluster_data)
    
    # Step 3 - Generate report
    report = generate_report(cluster_data, issues, recommendations, scripts)
    
    # Step 4 - Print report
    print(report)
    
    # Step 5 - Save report
    report_file = f"sre_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(report_file, 'w') as f:
        f.write(report)
    
    print(f"\n✅ Report saved to: {report_file}")

if __name__ == "__main__":
    main()
