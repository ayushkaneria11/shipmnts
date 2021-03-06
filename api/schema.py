from django.contrib.auth.models import User
import graphene
from graphene_django import DjangoObjectType
import graphql_jwt
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
        user = info.context.user
        question = Question(body=questionBody, title=questionTitle, user=user)
        question.save() 
        for tag in tags:
            # print(tag)
            tag_obj, created = Tag.objects.get_or_create(name=tag.lower())
            tag_obj.save() 
            tag_obj.questions.add(question)

        return CreateQuestion(question=question)

# Update Question Mutation
class UpdateQuestion(graphene.Mutation):
    question = graphene.Field(QuestionType)

    class Arguments:
        questionId = graphene.Int()
        questionTitle = graphene.String()
        questionBody = graphene.String()
        tags = graphene.List(graphene.String)

    def mutate(self, info, questionId, questionTitle, questionBody, tags):
        user = info.context.user
        question = Question.objects.get(pk=questionId)
        question.title = questionTitle
        question.body = questionBody
        question.save()
        for tag in tags:
            # print(tag)
            tag_obj, created = Tag.objects.get_or_create(name=tag.lower())
            tag_obj.save() 
            tag_obj.questions.add(question)

        return UpdateQuestion(question=question)

# Create Answer Mutation
class CreateAnswer(graphene.Mutation):
    answer = graphene.Field(AnswerType)

    class Arguments:
        answerBody = graphene.String()
        questionId = graphene.Int()

    def mutate(self, info, answerBody, questionId):
        question = Question.objects.get(id=questionId)
        user = info.context.user
        answer = Answer(body=answerBody, question=question,user=user)
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

# Accept Answer
class AcceptAnswer(graphene.Mutation):
    answer = graphene.Field(AnswerType)

    class Arguments:
        answerId = graphene.Int()
        questionId = graphene.Int()

    def mutate(self, info, answerId, questionId):
        question = Question.objects.get(id=questionId)
        answer = Answer.objects.get(id=answerId)

        # question.accepted_answer = answer
        if question.has_accepted_answer==False:
            answer.is_accepted = True
            question.has_accepted_answer= True
            question.save()
            answer.save()
        else:
            
            raise Exception('Question already has accepted answer!')

        return AcceptAnswer(answer=answer)

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
    accept_answer = AcceptAnswer.Field()
    update_question = UpdateQuestion.Field()


class Query(graphene.ObjectType):
    question = graphene.Field(QuestionType, id=graphene.Int())
    # answer = graphene.Field(AnswerType, id=graphene.Int())
    all_questions = graphene.List(QuestionType)
    all_answers = graphene.List(AnswerType)
    all_tags = graphene.List(TagType)
    question_by_tag = graphene.List(QuestionType, tag=graphene.String())
    question_by_user = graphene.List(QuestionType, user=graphene.Int())

    # resolvers for Queries
    def resolve_question(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Question.objects.get(pk=id)

        return None
    
    # def resolve_answer(self, info, **kwargs):
    #     id = kwargs.get('id')

    #     if id is not None:
    #         return Answer.objects.get(pk=id)

    #     return None

    def resolve_all_questions(self, info, **kwargs):
        return Question.objects.all()

    def resolve_all_answers(self, info, **kwargs):
        return Answer.objects.all()
    
    def resolve_all_tags(self, info, **kwargs):
        return Tag.objects.all()

    def resolve_question_by_tag(self, info, **kwargs):
        tag = kwargs.get('tag')

        if tag is not None:
            return Question.objects.filter(tags__name=tag)

        return None

    def resolve_question_by_user(self, info, **kwargs):
        user = kwargs.get('user')

        if user is not None:
            return Question.objects.filter(user=user)

        return None
