from django.test import TestCase
from django.utils import timezone
from .models import Question, Choice
import datetime
from django.urls import reverse


class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose
        pub_date is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose
        pub_date is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose
        pub_date is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


def create_question(question_text, days):
    """
    Create a question with the given `question_text` and publish the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions yet to be published.
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):

    def test_no_questions(self):
        """
        If not questions exists, an appropriate message is displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the index page.
        """
        create_question(question_text="This is a past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: This is a past question.>']
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future are not displayed on the index page.
        """
        create_question(question_text="This is a future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_and_future_questions(self):
        """
        Even if both exist, only questions from the past are displayed.
        """
        create_question(question_text="This is a past question.", days=-30)
        create_question(question_text="This is a future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: This is a past question.>']
        )

    def test_two_past_questions(self):
        """
        The index page can display multiple questions.
        """
        create_question(question_text="This is a past question.", days=-30)
        create_question(question_text="This is another past question.", days=-20)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [
                '<Question: This is another past question.>',
                '<Question: This is a past question.>'
            ]
        )


class QuestionDetailViewTest(TestCase):

    def test_future_question(self):
        """
        The details view of a question with a future pub_date returns a
        404 not found.
        """
        future_question = create_question(question_text="This is a future question.", days=30)
        url = reverse('polls:details', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The details view of a question with a past pub_date displays
        the question's text (question_text).
        """
        past_question = create_question(question_text="This is a past question.", days=-30)
        url = reverse('polls:details', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)


class QuestionResultsViewTest(TestCase):

    def test_future_question(self):
        """
        The details view of a question with a future pub_date returns a
        404 not found.
        """
        future_question = create_question(question_text="This is a future question.", days=30)
        url = reverse('polls:results', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The results view of a question with a past pub_date displays
        the question's text (question_text) and its voting options (if any).
        """
        past_question = create_question(question_text="This is a past question.", days=-30)
        past_question.choice_set.create(choice_text="This is a voting option.")
        url = reverse('polls:results', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
        self.assertContains(response, "This is a voting option.")

