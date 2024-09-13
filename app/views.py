from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import media
import json

@csrf_exempt  # Disable CSRF protection for simplicity; enable it in production and handle CSRF tokens properly.
def index(request):
    if request.method == "GET":
        # Handle GET request: retrieve all media objects.
        medias = media.objects.all()
        return render(request, "index.html", {"medias": medias})

    elif request.method == "POST":
        # Handle POST request: create a new media object.
        data = json.loads(request.body)  # Expecting JSON payload
        new_media = media.objects.create(**data)
        return JsonResponse({"id": new_media.id, "message": "Media created successfully."}, status=201)

    elif request.method == "PUT":
        # Handle PUT request: update an existing media object.
        data = json.loads(request.body)  # Expecting JSON payload
        print(data.get("user_id"))
        user_id = data.get("user_id")
        if not user_id:
            return JsonResponse({"error": "User ID is required to update media."}, status=400)

        # Fetch media objects with the provided user_id
        media_objects = media.objects.filter(user_id=user_id)

        if not media_objects.exists():
            return JsonResponse({"error": "No media found with the given user ID."}, status=404)

        # Update the fields of the media objects.
        updated_count = 0
        for media_obj in media_objects:
            for key, value in data.items():
                if hasattr(media_obj, key):
                    setattr(media_obj, key, value)
            media_obj.save()
            updated_count += 1

        return JsonResponse({"message": f"Media updated successfully for {updated_count} record(s)."}, status=200)

    else:
        # Method not allowed
        return JsonResponse({"error": "Method not allowed."}, status=405)
