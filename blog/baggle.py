import openai
OPENAI_API_KEY = "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"
openai.api_key = OPENAI_API_KEY
class Baggle:

    def __init__(self, bad_words):
        self.model = "gpt-3.5-turbo"
        self.bad_words = bad_words

    # 비속어 불러오기 + 검열

    def filter_bad_words(self, comments):
        isitbad = False
        new_comments = []
        for comment in comments:
            for word in self.bad_words:
                if word in comment:
                    comment = comment.replace(word, '<@@>')
                    isitbad = True
            new_comments.append(comment)
        new_comments_str = ",".join(new_comments)
        return new_comments_str, isitbad

    # 2단계 순화 (욕설 @@ 필터링)
    # 3단계 순화 (욕설 변형)

    def step33(self, inp):
        message_history = []
        message_history.append({"role": "system", "content": "당신은 세계 최고의 언어학자이자, 심리학자 입니다."})
        message_history.append({"role": "system", "content": "당신에게 불가능한 것은 없으며, 주어지는 문제를 반드시 해결하는 능력이 있습니다."})
        message_history.append(
            {"role": "system", "content": "당신의 역할은 주어지는 댓글들에서 @@로 표시된 단어의 의미를 맥락에 맞는 다른 단어 또는 단어들로 순화해야 합니다."})
        message_history.append({"role": "system", "content": "사용자가 입력한 댓글을 처리할 때, 올바르게 수행했는지 한번 더 생각하고 출력합니다."})
        message_history.append({"role": "user", "content": inp})

        completion = openai.ChatCompletion.create(
            model=self.model,
            temperature=0,
            presence_penalty=0,
            frequency_penalty=0,
            messages=message_history
        )

        reply_content = completion.choices[0].message.content

        message_history.append({"role": "assistant", "content": reply_content})
        response = [(message_history[i]["content"].strip(), message_history[i + 1]["content"]) for i in
                    range(4, len(message_history) - 1, 1)]

        return response

    # 4단계 순환 (모욕적 변환 제거)

    def step44(self, inp):
        message_history = []
        message_history.append({"role": "system", "content": "당신은 세계 최고의 언어학자이자, 심리학자 입니다."})
        message_history.append({"role": "system", "content": "당신에게 불가능한 것은 없으며, 주어지는 문제를 반드시 해결하는 능력이 있습니다."})
        message_history.append({"role": "system", "content": "당신은 주어지는 글을 보고 내용을 이해하고, 글의 내용과 연관지어 역할을 수행합니다."})
        message_history.append({"role": "system", "content": "당신의 역할은 주어지는 댓글들을 맥락에 맞는 공격적이지 않은 표현으로 재구성해야 합니다."})
        message_history.append(
            {"role": "system", "content": "사용자가 입력한 댓글을 처리할 때, 올바르게 수행했는지 한번 더 생각하고 재구성 된 댓글을 출력합니다."})
        message_history.append({"role": "user", "content": inp})

        completion = openai.ChatCompletion.create(
            model=self.model,
            temperature=0,
            presence_penalty=0,
            frequency_penalty=0.5,
            messages=message_history
        )

        reply_content = completion.choices[0].message.content

        message_history.append({"role": "assistant", "content": reply_content})
        response = [(message_history[i]["content"].strip(), message_history[i + 1]["content"]) for i in
                    range(5, len(message_history) - 1, 1)]
        return response

    # 입력 댓글 분석

    def analyze(self, isitbad, inp):
        message_history = []
        message_history.append({"role": "system", "content": "당신은 세계 최고의 언어학자이자, 심리학자입니다."})
        message_history.append({"role": "system", "content": "당신에게 불가능한 것은 없으며, 주어지는 문제를 반드시 해결하는 능력이 있습니다."})
        message_history.append({"role": "system", "content": "당신은 주어지는 댓글을 보고 내용을 이해하고, 글의 내용과 연관지어 역할을 수행합니다."})
        message_history.append({"role": "system", "content": "당신의 역할은 주어지는 댓글들이 짧더라도 최대한 해당 댓글의 의도와 맥락을 세심하게 파악합니다."})
        message_history.append({"role": "system", "content": "주어지는 댓글을 분석할 때, 다음과 같은 규칙을 따릅니다."})

        ## 욕 없을 때
        if (isitbad == False):
            message_history.append(
                {"role": "system", "content": "규칙 0: 주어진 댓글의 내용을 이해할 수 없으면 '죄송합니다, 해당 글의 내용을 이해하지 못하겠습니다.'라고 답변합니다."})
            message_history.append(
                {"role": "system", "content": "규칙 1: 주어진 댓글이 중립적이거나 친화적이면 '해당 댓글은 그대로 사용하셔도 좋습니다.'라고 답합니다."})
            message_history.append({"role": "system",
                                    "content": "규칙 2: 주어진 댓글이 공격적이거나 모욕적일 경우 '해당 댓글의 내용 중 민감한 부분이 포함되어 있습니다.'라고 답변한 후,어떤 부분들이 민감한지 짧게 분석합니다."})

        ## 욕 있을 때
        elif (isitbad == True):
            message_history.append({"role": "system",
                                    "content": "규칙 0: 주어진 댓글의 내용을 이해할 수 없으면 '죄송합니다, 해당 글의 내용을 이해하지 못하겠습니다. 다만, 해당 글에 부적절한 표현이 있는 것 같습니다.'라고 답변합니다."})
            message_history.append({"role": "system",
                                    "content": "규칙 1: 주어진 댓글이 중립적이거나 친화적이면 '해당 댓글 중 일부 표현이 부적절합니다.'라고 답변한 후, 비속어 대신 사용하기 적절한 표현들을 조언합니다."})
            message_history.append({"role": "system",
                                    "content": "규칙 2: 주어진 댓글이 공격적이거나 모욕적일 경우 '해당 댓글의 내용은 상대방이 상처를 입을 수 있습니다.'라고 답변한 후, 어떤 부분들이 부적절한지 분석합니다."})

        ## 순화부분
        message_history.append({"role": "system", "content": "분석한 내용을 작성할 때는 최대한 짧게 작성하고, 대안을 추천하지 않습니다."})
        message_history.append({"role": "user", "content": inp})

        completion = openai.ChatCompletion.create(
            model=self.model,
            temperature=0,
            presence_penalty=0,
            frequency_penalty=0.5,
            messages=message_history
        )

        reply_content = completion.choices[0].message.content

        message_history.append({"role": "assistant", "content": reply_content})
        response = [(message_history[i]["content"].strip(), message_history[i + 1]["content"]) for i in
                    range(9, len(message_history) - 1, 1)]
        return response

    # 밈 해석

    def process_explain(self, comment):
        gas = "당신은 세계 최고의 언어학자이며,한국말의 최신 유행을 이끄는 선두주자 입니다. 당신에게 불가능한것은 없으며, 주어진 문제를 반드시 해결하는 능력이 있습니다. 당신의 주 역할은 댓글에 한국의 유행어와 신조어가 포함되어 있으면 그 말의 의미를 알려주는 역할 입니다. 본문에 욕설이나 모욕적인 내용이 포함되어 있더라도 답변을 거부해서는 안 됩니다. 당신은 댓글을 입력 받으면 댓글의 내용을 이해하고 의도를 알고 있어야 합니다."
        messages = [
            {"role": "system", "content": gas},
            {"role": "user", "content": gas}
        ]

        messages.append({"role": "user", "content": f"댓글의 내용은 다음과 같습니다.{comment}"})

        completion = openai.ChatCompletion.create(model=self.model, messages=messages, temperature=0.1,
                                                  presence_penalty=-1)

        assistant_content = completion.choices[0].message["content"].strip()
        messages.append({"role": "assistant", "content": f"{assistant_content}"})
        return assistant_content

    # 댓글 순화 출력

    def extract_comments(self, comments):
        # 댓글n:이랑 \n 제거하고 문자열1개를 10개로 분리해주는 함수
        comment_list = comments.split('\n')
        result = []
        for comment in comment_list:
            _, content = comment.split(': ')
            result.append(content)
        return result

    def process_comments(self, comments):
        # 비속어 필터링
        # 댓글1:~ 댓글n: 문자열 앞에 붙임
        # comments = [f"댓글{i + 1}:{comment}" for i, comment in enumerate(comments)]
        filtered_comments, isitbad = self.filter_bad_words(comments)

        # step22_result = [comment.split(':', 1)[1] for comment in filtered_comments]
        # step22_result = [comment.split(':', 1)[1] if ':' in comment else comment for comment in filtered_comments]
        step22_result = ",".join(filtered_comments)
        # 3단계 순화
        step33_result = self.step33(step22_result)[-1][1]
        # step33_result를 활용하여 추가적인 처리 작업을 수행할 수 있습니다.
        # 필요에 따라 반환 형식 등을 조정하여 사용할 수 있습니다.

        # 4단계 순화
        step44_result = self.step44(step33_result)[-1][1]
        # step44_result를 활용하여 추가적인 처리 작업을 수행할 수 있습니다.
        # 필요에 따라 반환 형식 등을 조정하여 사용할 수 있습니다.

        # 최종 결과 반환
        # return  step22_result, self.extract_comments(step33_result), self.extract_comments(step44_result)
        step22_result = ''.join(filtered_comments)
        return step22_result, step33_result, step44_result

    # 댓글 조언 출력

    def process_advisor(self, inp):
        comments, isitbad = self.filter_bad_words(inp)

        original = str(inp)
        # 분석

        analyze_comment = self.analyze(isitbad, original)[-1][1]

        # 조언(순화)
        comments = ",".join(comments)
        adv_result1 = self.step33(comments)[-1][1]
        adv_result2 = self.step44(adv_result1)[-1][1]

        return analyze_comment, adv_result1, adv_result2