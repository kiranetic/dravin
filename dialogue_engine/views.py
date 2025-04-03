from django.shortcuts import render

# Create your views here.

from rest_framework import generics, status
from rest_framework.response import Response
from .models import Query
from .serializers import QuerySerializer
from .preprocess import preprocess_text
from .classifier import train_classifier, predict_label

# Dummy training data (replace with real dataset later)
TRAINING_TEXTS = ["How do I reset?", "What’s my bill?", "Help me login"]
TRAINING_LABELS = ["technical", "billing", "technical"]

class QueryList(generics.ListCreateAPIView):
    queryset = Query.objects.all()
    serializer_class = QuerySerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Train classifier (in practice, load a pre-trained model)
        features, vectorizer = preprocess_text(TRAINING_TEXTS)
        clf = train_classifier(features, TRAINING_LABELS)
        # Predict label for new query
        new_features = vectorizer.transform([request.data['text']])
        predicted_label = predict_label(clf, new_features)[0]
        # Save with predicted label
        query_instance = serializer.save(label=predicted_label)
        # Return full serialized response
        response_serializer = self.get_serializer(query_instance)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
