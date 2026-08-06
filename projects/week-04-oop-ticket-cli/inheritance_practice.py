class Employee:
    def __init__(self, name: str) -> None:
        self.name = name

    def get_role_description(self) -> str:
        return f"Employee: {self.name}"


class SupportAgent(Employee):
    def __init__(self, name: str, queue_name: str) -> None:
        super().__init__(name)
        self.queue_name = queue_name

    def get_role_description(self) -> str:
        return f"Support Agent: {self.name} | Queue: {self.queue_name}"


def main() -> None:
    employee = Employee("Furkan")
    print(employee.get_role_description())

    agent = SupportAgent("Furkan", "Technical Support")
    print(agent.get_role_description())


if __name__ == "__main__":
    main()