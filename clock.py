from typing import List, Optional, Tuple, Union


class LightClock:
    def __init__(
        self,
        sequence: List[Tuple[Union[None, str, Tuple[str, ...]], float]],
        # pause_duration: float = 1.0,
    ) -> None:
        self.sequence: List[
            Tuple[Optional[Union[str, Tuple[str, ...]]], float]
        ] = []
        self.current_directions: Optional[Union[str, Tuple[str, ...]]] = None
        for letter, duration in sequence:
            self.sequence.append((letter, duration))
            # self.sequence.append((None, pause_duration))

        self.current_index: int = 0
        self.current_directions, self.duration = self.sequence[0]
        self.elapsed: float = 0.0

    def update(self, dt: float) -> None:
        self.elapsed += dt

        if self.elapsed >= self.duration:
            self.current_index = (self.current_index + 1) % len(self.sequence)
            self.current_directions, self.duration = self.sequence[
                self.current_index
            ]
            self.elapsed = 0.0

    def get_current_directions(self) -> Optional[Union[str, Tuple[str, ...]]]:
        return self.current_directions
