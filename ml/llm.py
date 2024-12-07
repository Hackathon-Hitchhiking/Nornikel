from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from llama_cpp import Llama

from config import ModelKwargs


class BaseLlama3Model(ABC):
    @abstractmethod
    def load_model(self, kwargs: ModelKwargs, model_path: str) -> None: ...

    @abstractmethod
    def inference(self, kwargs: Optional[ModelKwargs] = None) -> str: ...

    @abstractmethod
    def add_message(self, role: str, content: str) -> None: ...

    @abstractmethod
    def clean_chat(self) -> None: ...

    @abstractmethod
    def print_chat(self) -> None: ...

    @abstractmethod
    def get_chat(self) -> List[Dict[str, str]]: ...


class LLama3Quantized(BaseLlama3Model):
    def __init__(self) -> None:
        super().__init__()
        self._llm: Optional[Llama] = None
        self._chat: List[Dict[str, str]] = []
        self._kwargs: ModelKwargs = ModelKwargs()

    def load_model(self, kwargs: ModelKwargs, model_path: str) -> None:
        if not model_path:
            raise ValueError("Путь к модели не может быть пустым.")
        self._llm = Llama(
            model_path=model_path,
            n_gpu_layers=-1,
            n_batch=512,
            n_ctx=kwargs.max_tokens,
            n_parts=1,
        )
        self._kwargs = kwargs

    def _check_model_loaded(self) -> None:
        if not self._llm:
            raise RuntimeError(
                "Модель не загружена. Пожалуйста, загрузите модель перед выполнением вывода."
            )

    def inference(self, kwargs: Optional[ModelKwargs] = None) -> str:
        self._check_model_loaded()
        if not kwargs:
            kwargs = self._kwargs
        if not self._chat:
            raise RuntimeError(
                "Чат пуст. Пожалуйста, добавьте сообщения в чат перед выполнением вывода."
            )
        return self._llm.create_chat_completion(
            self._chat,
            temperature=kwargs.temperature,
            top_k=kwargs.top_k,
            top_p=kwargs.top_p,
            repeat_penalty=kwargs.repeat_penalty,
            stream=False,
        )["choices"][0]["message"]["content"]

    def add_message(self, role: str, content: str) -> None:
        if not role or not content:
            raise ValueError("Роль и содержание не могут быть пустыми.")
        self._chat.append({"role": role, "content": content})

    def clean_chat(self) -> None:
        self._chat = []

    def get_chat(self) -> List[Dict[str, str]]:
        return self._chat
