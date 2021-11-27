import graphene
from graphene_django import DjangoObjectType

from .models import Question, Answer


# Question Type
class QuestionType(DjangoObjectType):
    class Meta:
        model = Question
    
# Answer Type
class AnswerType(DjangoObjectType):
    class Meta:
        model = Answer


class Query(graphene.ObjectType):
    question = graphene.Field(QuestionType, id=graphene.Int())
    all_questions = graphene.List(QuestionType)
    all_answers = graphene.List(AnswerType)

    # resolvers for Queries
    def resolve_question(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Question.objects.get(pk=id)

        return None

    def resolve_all_questions(self, info, **kwargs):
        return Question.objects.all()

    def resolve_all_answers(self, info, **kwargs):
        return Answer.objects.all()
