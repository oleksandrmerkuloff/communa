# from rest_framework.viewsets import ModelViewSet

# from .serializers import PetitionReaderSerializer, PetitionWriterSerializer, VoteSerializer
# from .models import PetitionVote, Petition


# class VoteViewSet(ModelViewSet):
#     queryset = PetitionVote.objects.all()
#     serializer_class = VoteSerializer

#     def get_queryset(self):
#         return (
#             PetitionVote.objects
#             .select_related("petition", "resident",)
#         )


# class PetitionViewSet(ModelViewSet):
#     queryset = Petition.objects.all()

#     def get_queryset(self):
#         return (
#             Petition.objects
#             .select_related("author", "organization")
#             .prefetch_related("votes")
#         )

#     def get_serializer_class(self):
#         if self.action in ("list", "retrieve"):
#             return PetitionReaderSerializer
#         return PetitionWriterSerializer
