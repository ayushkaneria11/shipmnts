from django.contrib.auth.models import User
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


# Create Question Mutation
class CreateQuestion(graphene.Mutation):
    question = graphene.Field(QuestionType)

    class Arguments:
        questionTitle = graphene.String()
        questionBody = graphene.String()
        tags = graphene.List(graphene.String)

    def mutate(self, info, questionTitle, questionBody, tags):
        question = Question(body=questionBody, title=questionTitle,tags=tags)
        question.save() 

        return CreateQuestion(question=question)

# Create Answer Mutation
class CreateAnswer(graphene.Mutation):
    answer = graphene.Field(AnswerType)

    class Arguments:
        answerBody = graphene.String()
        questionId = graphene.Int()

    def mutate(self, info, answerBody, questionId):
        question = Question.objects.get(id=questionId)
        answer = Answer(body=answerBody, question=question)
        answer.save()

        return CreateAnswer(answer=answer)

class Mutation(graphene.ObjectType):
    create_question = CreateQuestion.Field()
    create_answer = CreateAnswer.Field()


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
