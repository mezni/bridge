package entities

import "sync"

// SequenceGenerator represents a sequence generator entity.
type SequenceGenerator struct {
	mu      sync.Mutex
	counter int64
	step    int64
	name    string
}

// NewSequenceGenerator creates a new SequenceGenerator instance.
func NewSequenceGenerator(name string, initialValue, step int64) *SequenceGenerator {
	return &SequenceGenerator{
		name:    name,
		counter: initialValue,
		step:    step,
	}
}

// Next generates the next number in the sequence.
func (s *SequenceGenerator) Next() int64 {
	s.mu.Lock()
	defer s.mu.Unlock()

	nextValue := s.counter
	s.counter += s.step
	return nextValue
}

// Current returns the current value without advancing the sequence.
func (s *SequenceGenerator) Current() int64 {
	s.mu.Lock()
	defer s.mu.Unlock()

	return s.counter
}

// Reset sets the sequence counter to a specified value.
func (s *SequenceGenerator) Reset(value int64) {
	s.mu.Lock()
	defer s.mu.Unlock()

	s.counter = value
}

// Name returns the name of the sequence.
func (s *SequenceGenerator) Name() string {
	return s.name
}
