from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.contrib.auth.views import LoginView
from .models import Container, WaterLevel, Alert


# =========================
# DASHBOARD PAGE (Chart loads here)
# =========================
@login_required
def water_chart(request):
    return render(request, "water_chart.html")
def home(request):
    return render(request, "home.html")


# =========================
# OPTIONAL: HTTP DATA (if you stop using WebSocket)
# =========================
@login_required
def water_level_data(request):
    records = WaterLevel.objects.order_by('-recorded_at')[:20]

    labels = []
    values = []

    for r in reversed(records):
        labels.append(r.recorded_at.strftime("%H:%M:%S"))
        values.append(r.depth)

    return JsonResponse({
        "labels": labels,
        "values": values
    })


# =========================
# LIVE SUMMARY (for cards / AJAX)
# =========================
@login_required
def live_summary(request):
   def live_summary(request):
    containers = Container.objects.all()

    data = []

    for c in containers:
        latest = c.water_levels.order_by('-recorded_at').first()

        data.append({
            "container": c.label,
            "depth": latest.depth if latest else 0,
            "time": latest.recorded_at.strftime("%H:%M:%S") if latest else None
        })

    return JsonResponse(data, safe=False)
# =========================
# ALERT LOG PAGE
# =========================
@login_required
def alerts_view(request):
    alerts = Alert.objects.order_by('-triggered_at')[:30]
    return render(request, "alerts.html", {"alerts": alerts})


# =========================
# STATISTICS PAGE
# =========================
@login_required
def stats_view(request):
    containers = Container.objects.all()
    stats = []

    for container in containers:
        avg_depth = container.water_levels.aggregate(avg=Avg('depth'))['avg']

        stats.append({
            "label": container.label,
            "average_depth": round(avg_depth, 2) if avg_depth else 0
        })

    return render(request, "stats.html", {"stats": stats})


# =========================
# ALERT CHECK FUNCTION
# =========================
def check_alert(container, depth):
    if container.alert_min is not None and depth < container.alert_min:
        return f"Low water level in {container.label}"

    if container.alert_max is not None and depth > container.alert_max:
        return f"High water level in {container.label}"

    return None


# =========================
# ADD SENSOR DATA (POST API)
# =========================
def add_water_level(request):
    if request.method == "POST":
        container_id = request.POST.get("container_id")
        depth = request.POST.get("depth")

        try:
            depth = float(depth)
        except:
            return JsonResponse({"error": "Invalid depth"}, status=400)

        container = get_object_or_404(Container, id=container_id)

        # Save data
        WaterLevel.objects.create(
            container=container,
            depth=depth
        )

        # Check alert
        alert_msg = check_alert(container, depth)

        if alert_msg:
            Alert.objects.create(
                container=container,
                message=alert_msg,
                level=depth
            )

        return JsonResponse({
            "status": "success",
            "depth": depth,
            "alert": alert_msg
        })

    return JsonResponse({"error": "Invalid request"}, status=400)


from django.contrib.auth import authenticate, login


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=email, password=password)

        if user:
            login(request, user)
            return redirect('/')
        else:
            return render(request, "login.html", {"error": "Invalid login"})

    return render(request, "login.html")