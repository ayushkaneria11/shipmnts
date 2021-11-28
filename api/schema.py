from django.contrib.auth.models import User
import graphene
from graphene_django import DjangoObjectType

from .models import Question, Answer,Tag


# Question Type
class QuestionType(DjangoObjectType):
    class Meta:
        model = Question
    
# Answer Type
class AnswerType(DjangoObjectType):
    class Meta:
        model = Answer

class TagType(DjangoObjectType):
    class Meta:
        model = Tag


# Create Question Mutation
class CreateQuestion(graphene.Mutation):
    question = graphene.Field(QuestionType)
    tags=  graphene.List(TagType)

    class Arguments:
        questionTitle = graphene.String()
        questionBody = graphene.String()
        tags = graphene.List(graphene.String)

    def mutate(self, info, questionTitle, questionBody, tags):

        question = Question(body=questionBody, title=questionTitle)
        question.save() 
        for tag in tags:
            # print(tag)
            tag_obj, created = Tag.objects.get_or_create(name=tag.lower())
            tag_obj.save() 
            tag_obj.questions.add(question)

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

# Upvote Mutations
class UpvoteQuestion(graphene.Mutation):
    question = graphene.Field(QuestionType)

    class Arguments:
        questionId = graphene.Int()

    def mutate(self, info, questionId):
        question = Question.objects.get(id=questionId)
        question.upvotes += 1
        question.save()

        return UpvoteQuestion(question=question)

# Downvote Mutations
class DownvoteQuestion(graphene.Mutation):
    question = graphene.Field(QuestionType)

    class Arguments:
        questionId = graphene.Int()

    def mutate(self, info, questionId):
        question = Question.objects.get(id=questionId)
        question.downvotes += 1
        question.save()

        return DownvoteQuestion(question=question)

class UpvoteAnswer(graphene.Mutation):
    answer = graphene.Field(AnswerType)

    class Arguments:
        answerId = graphene.Int()
        # questionId = graphene.Int()

    def mutate(self, info, answerId):
        # question = Question.objects.get(id=questionId)
        # answer = Answer.
        answer = Answer.objects.get(id=answerId)

        answer.upvotes += 1
        answer.save()

        return UpvoteAnswer(answer=answer)

class DownvoteAnswer(graphene.Mutation):
    answer = graphene.Field(AnswerType)

    class Arguments:
        answerId = graphene.Int()
        # questionId = graphene.Int()

    def mutate(self, info, answerId):
        # question = Question.objects.get(id=questionId)
        # answer = Answer.
        answer = Answer.objects.get(id=answerId)

        answer.downvotes += 1
        answer.save()

        return DownvoteAnswer(answer=answer)

# # Create tag
class CreateTag(graphene.Mutation):
    tag = graphene.Field(TagType)

    class Arguments:
        tagName = graphene.String()

    def mutate(self, info, tagName):
        tag = Tag(name=tagName)
        tag.save()

        return CreateTag(tag=tag)

# add tag to question
# class AddTagToQuestion(graphene.Mutation):
#     question = graphene.Field(QuestionType)

#     class Arguments:
#         questionId = graphene.Int()
#         tagName = graphene.String()

#     def mutate(self, info, questionId, tagName):
#         question = Question.objects.get(id=questionId)
#         tag = Tag.objects.get(name=tagName)
#         question.tags.add(tag)
#         question.save()

#         return AddTagToQuestion(question=question)


# get all tags


class Mutation(graphene.ObjectType):
    create_question = CreateQuestion.Field()
    create_answer = CreateAnswer.Field()
    upvote_question = UpvoteQuestion.Field()
    downvote_question = DownvoteQuestion.Field()
    upvote_answer = UpvoteAnswer.Field()
    downvote_answer = DownvoteAnswer.Field()
    create_tag = CreateTag.Field()


class Query(graphene.ObjectType):
    question = graphene.Field(QuestionType, id=graphene.Int())
    all_questions = graphene.List(QuestionType)
    all_answers = graphene.List(AnswerType)
    all_tags = graphene.List(TagType)

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
    
    def resolve_all_tags(self, info, **kwargs):
        return Tag.objects.all()
