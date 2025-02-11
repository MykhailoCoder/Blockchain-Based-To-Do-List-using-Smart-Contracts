// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract TodoList {
    struct Task {
        uint id;
        string description;
        bool completed;
    }

    Task[] public tasks;
    uint public taskCount;

    event TaskAdded(uint id, string description);
    event TaskCompleted(uint id);

    function addTask(string memory _description) public {
        tasks.push(Task(taskCount, _description, false));
        emit TaskAdded(taskCount, _description);
        taskCount++;
    }

    function getTask(uint _id) public view returns (string memory, bool) {
        require(_id < taskCount, "Task does not exist");
        Task storage task = tasks[_id];
        return (task.description, task.completed);
    }

    function completeTask(uint _id) public {
        require(_id < taskCount, "Task does not exist");
        tasks[_id].completed = true;
        emit TaskCompleted(_id);
    }

    function getAllTasks() public view returns (Task[] memory) {
        return tasks;
    }
}
